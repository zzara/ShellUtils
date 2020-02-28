package main

import (
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"strconv"

	imap "github.com/emersion/go-imap"
	"github.com/emersion/go-imap/client"
	"github.com/emersion/go-message/charset"
	"github.com/emersion/go-message/mail"
)

// SET ENVIRONMENT VARIABLES:
//export DATABASE_CONNECTION_STRING=outlook.office365.com:993
//export DBUSR=<email>
//export DBPWD=<password>
//export SOURCE_FOLDER=<folder>
//export NUM_MSG_PROCESS=<count>

// USAGE:
// Example: ./puller -apath="/Users/<user>/Desktop/attachments" -epath="/Users/<user>/Desktop/emails"
//			./puller --apath "/Users/<user>/Desktop/attachments" --epath "/Users/<user>/Desktop/emails"
// Default folder is /tmp if no path is supplied

var apath = flag.String("apath", "/tmp", "path to store attachments")
var epath = flag.String("epath", "/tmp", "path to store attachments")

// Write out the buffered content
func fileHandler(path string, name uint32, filename string, file []byte) {
	location := fmt.Sprintf("%s/%d_%s", path, name, filename)
	_ = ioutil.WriteFile(location, file, 0644)
	return
}

func main() {
	flag.Parse()

	// Charset reader for message encodings
	imap.CharsetReader = charset.Reader

	// Verify environment variables.
	dbConnStr, errEnv := os.LookupEnv("DATABASE_CONNECTION_STRING")
	if errEnv == false {
		log.Fatal("errorSetEnv = DATABASE_CONNECTION_STRING")
	}
	dbUsr, errEnv := os.LookupEnv("DBUSR")
	if errEnv == false {
		log.Fatal("errorSetEnv = DBUSR")
	}
	dbPwd, errEnv := os.LookupEnv("DBPWD")
	if errEnv == false {
		log.Fatal("errorSetEnv = DBPWD")
	}
	sourceFolder, errEnv := os.LookupEnv("SOURCE_FOLDER")
	if errEnv == false {
		log.Fatal("errorSetEnv = SOURCE_FOLDER")
	}
	numMsgProcess, errEnv := os.LookupEnv("NUM_MSG_PROCESS")
	if errEnv == false {
		log.Fatal("errorSetEnv = NUM_MSG_PROCESS")
	}
	cntMsgProcess, errConv := strconv.ParseUint(numMsgProcess, 10, 32)
	if errConv != nil {
		log.Fatalf("errorSetEnv = NUM_MSG_PROCESS e = %v", errConv)
	}

	// Connect to outlook server.
	conn, err := client.DialTLS(dbConnStr, nil)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Logout()
	log.Println("Successful connection to server.")

	// Login to mailbox.
	if err := conn.Login(dbUsr, dbPwd); err != nil {
		log.Fatal(err)
	}
	log.Println("Successful login.")

	// Select source folder.
	mailBox, err := conn.Select(sourceFolder, false)
	if err != nil {
		log.Fatal(err)
	}

	var cntMsgs = uint32(cntMsgProcess)
	from := uint32(1)
	to := mailBox.Messages
	if mailBox.Messages > cntMsgs {
		from = mailBox.Messages - cntMsgs - 1
	}

	log.Printf("%d messages total in inbox\n", to)

	seqSet := new(imap.SeqSet)
	seqSet.AddRange(from, to)

	messages := make(chan *imap.Message, cntMsgs)
	done := make(chan error, 1)

	// Get the whole message body
	section := &imap.BodySectionName{}
	items := []imap.FetchItem{section.FetchItem()}

	// Goroutine to retrieve messages.
	go func() {
		done <- conn.Fetch(seqSet, items, messages)
	}()

	log.Printf("Last %v messages:\n", cntMsgs)

	// Parse the emails
	cnt := 1
	for msg := range messages {

		r := msg.GetBody(section)
		if r == nil {
			//log.Fatal("Server didn't returned message body")
			fmt.Printf("process=get_body message=server_no_message_body\n")
		}

		// Create a new mail reader
		mr, err := mail.CreateReader(r)
		if err != nil {
			//log.Fatal(err)
			fmt.Println(err)
		}

		part_count := 1
		// Process each message's part
		for {
			part_count += 1
			p, err := mr.NextPart()
			if err == io.EOF {
				break
			} else if err != nil {
				//log.Fatal(err)
				fmt.Printf("process=get_part error=%s\n", err)
			}

			switch h := p.Header.(type) {
			case *mail.InlineHeader:
				log.Printf(" %v * %v part %d", cnt, msg.SeqNum, part_count)
				// This is the message's text (can be plain-text or HTML)

				// Get email subject
				var filename string
				header := mr.Header
				if subject, err := header.Subject(); err == nil {
					filename = fmt.Sprintf("%s_%d.eml", subject, part_count)
				} else {
					filename = fmt.Sprintf("subject_%d.eml", part_count)
				}

				body, err := ioutil.ReadAll(p.Body)
				if err != nil {
					//log.Fatal(err)
					fmt.Printf("process=get_body error=%s\n", err)
				}

				log.Printf("process=get_body message=got_text msg_subject=%d_%s\n", msg.SeqNum, filename)

				// Write email body part to file
				go fileHandler(*epath, msg.SeqNum, filename, body)

			case *mail.AttachmentHeader:
				// This is an attachment
				filename, _ := h.Filename()

				if filename == "" {
					filename = fmt.Sprintf("%d.unknown", msg.SeqNum)
				}

				log.Printf(" %v * %v got attachment: %v\n", cnt, msg.SeqNum, filename)

				// Process message part for attachments ttachments
				attachment, err := ioutil.ReadAll(p.Body)
				if err != nil {
					//log.Fatal(err)
					fmt.Printf("process=get_attachment error=%s\n", err)
				}

				// Write email attachment to file
				go fileHandler(*apath, msg.SeqNum, filename, attachment)
			}
		}
		part_count = 1
		cnt++
	}

	if err := <-done; err != nil {
		log.Fatal(err)
	}
}
