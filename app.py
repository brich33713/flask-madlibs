from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from stories import Story

app = Flask(__name__)
app.config['SECRET_KEY'] = "string"
debug = DebugToolbarExtension(app)

story = Story(["place", "noun", "verb", "adjective", "plural_noun"],
    "Once upon a time in a long-ago {place}, there lived a large {adjective} {noun}. It loved to {verb} {plural_noun}.","story1")

#Uncomment to unlock the story selection option
story2 = Story(["adjective","noun","verb_past_tense","adverb","adjective2",
"noun2","noun3","adjective3","verb2","adverb2"],
"""Today I went to the zoo. I saw a(n) {adjective}
{noun} jumping up and down in its tree. He {verb_past_tense} {adverb}
through the large tunnel that led to its {adjective2} {noun2}. 
I got some peanuts and passed them through the cage to a gigantic gray {noun3}
towering above my head. Feeding that animal made me hungry. 
I went to get a {adjective3} scoop of ice cream. It filled my stomach. 
Afterwards I had to {verb2} {adverb2} to catch our bus.""", "story2")

stories = [story,story2]
@app.route("/")
def homepage():
    
    return render_template("base.html",stories=stories)

@app.route("/inputs")
def storyPrompts():
    story_choice = request.args["Story"]
    return render_template("inputs.html",prompts=stories[int(story_choice)].prompts,story_choice=story_choice)

@app.route("/story")
def genStory():
    ans = {}
    story_choice = request.args["story_choice"]
    for prompt in stories[int(story_choice)].prompts:
        ans[prompt] = request.args[f"{prompt}"]
    return render_template("story.html", story=stories[int(story_choice)].generate(ans), title=story.title)