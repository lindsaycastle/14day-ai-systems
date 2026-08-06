#### Youtube recomendations ####
Deliver appropriate, user tailored videos with user input from youtube.

### Who uses the system  ###
Jessie and I, We watch TV but the youtube recomendations are garbae.

### what does success look like ###
- Videos that have been viewed before are not shown.
- There is a mix of new and familar content
- Certain categories like Music, Stand up routines are excluded

### what would be a failure ###
- repeated videos
- previous requests not being honoured
- high token use



### input ####
requests
- show user videos
- show user certain types of videos
- dont show me these videos
- never show this video

data
- user input.txt
- db of previously watched videos.??
- current youtube selection of videos. list of videos
- previous watch habbits.???
- Current user . list of users
- Previous requests - table of requests


### Processing ###
pre:
add system prompt
add dev prompt
test prompt for clarity and validity:
- prompt is asking for a type or mood of videos
- prompt is asking for specific change to context

package request
add output format if not specified

post:
check against watched vids list 

### Model ###

Do the work
Hybrid - recomender


### Output ####

return response.  feedback on if task was done, text string
followup questions if needed . prompt for user tpo continue
list of videos . list of video ids for app to interpreate
api responses if needed .python triggers

### feedback  ###
update context docs
apply followup answers

