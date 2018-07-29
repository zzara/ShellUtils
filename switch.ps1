switch ( (Get-Date).DayOfWeek ) {
"Sunday"
{"It’s the weekend but work tomorrow"; break}
"Monday"
{"Back to work"; break}
"Tuesday"
{"Long time until Friday"; break}
"Wednesday" {"Half way through the week"; break}
"Thursday" {"Friday tomorrow"; break}
"Friday"
{"It’s the weekend tomorrow"; break}
"Saturday" {"It’s the weekend"; break}
default
{"Something's gone wrong"}
}
