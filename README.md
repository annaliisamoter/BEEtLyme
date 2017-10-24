# BEEtLyme
A web app for those treating Lyme disease to more easily track symptoms and treatments, and visualize efficacy over time.

##Contents
* Tech Stack
* Why BEEtLyme?
* Features
* Installation
* About Me

##Tech Stack
* Backend: Python, Flask, PostgreSQL, SQLAlchemy
* Frontend: Javascript, jQuery, AJAX, HTML5, CSS3, Bootstrap
* APIs: Plotly.js, jQuery Easy-Autofill, Ajax Bootstrap datepicker plugin.

##Why BEEtLyme?

The CDC estimates that every year around 300,000 new people contract Lyme disease (borreliosis) in the US alone.  Only about 30,000 of 
those are reported to the CDC, due to inaccurate lab testing and reporting guidelines that are too strict.  This means that the majority
of people who contract Lyme disease go undiagnosed, often for many years.  Once the infection becomes late-stage (meaning it is not caught
within the first 6 months of infection), Lyme disease is notoriously intractable and difficult to treat.  Treatment can take many years,
with many remissions and relapses.  It can be difficult for Lyme patients to get a sense of whether a treatment is working or not, since
symptoms are so varied and can come and go.  We need a better way to keep track of symptom intensity and treatments, in a way that allows
for visualization of efficacy over time.

##Features

<img src="https://www.evernote.com/l/AMsihbKslMdGhpVJhBD2-OaXRgYwWzKji00B/image.png" alt="BEEtLyme_Homepage" />

Once logged in, the User* is redirected to the profile page, which displays the Symptoms and Treatments they are currently tracking, 
along with any journal entries in the database.
*Note* this is a ficticious User for the purpose of demo only.

<img src="https://www.evernote.com/l/AMuP4loIg1xB-ppv7DyfaQrCjaPVaklopg0B/image.png" alt="BEEtLyme_Profile" />

The user can choose new Symptoms or Treatments to track on the "/set" page, with autofill options queried from the database via Ajax 
using jquery Ease Autofill.  Or they can create their own, which will be added to the database for future users to choose from. 
This cuts down on repetition in the database due to misspellings or small variations in expression.

<img src="https://www.evernote.com/l/AMsncNLG8CtPvIW3FWfAgvZ6FI59yQUZRMoB/image.png" alt="BEEtLyme_Set" />

On the "/track" page, the User can choose a date with the Ajax Bootstrap Datepicker plugin.  Values for Symptom Intensity (limited to
integers from 0-10) and dosage of Treatments can be submitted, as well as a Journal Entry.  Each form is submitted via Ajax calls without 
refereshing the page for a smoother User Experience.

<img src="https://www.evernote.com/l/AMt06oFvFftMp4NdOiznkfYYEGB77OxuM3wB/image.png" alt="BEEtLyme_Track" />

The most important feature of the project is the graphing option, which allows the User to visualize symptoms over time with a treatment 
overlay. The User is able to choose up to (3) Symptoms and (1) Treatment to graph on the "/graph" page. 

<img src="https://www.evernote.com/l/AMsp20j2bS1OBrXn4f8wBMJ_zARRaXdCLMwB/image.png" alt="BEEtLyme_Graph_Options" />

These choices are then relayed to the next page where an ajax call is made to a route that queries the database.  The data is then repackaged
with the aid of helper functions into the proper format for the plotly.js to display.

<img src="https://www.evernote.com/l/AMuAGnVxeThHf5pjIEDFAaN3wKkgnvgvl8YB/image.png" alt="BEEtLyme_plotly" />

The biggest challenge of this project was to choose a visualization API that would allow me the flexibility yet complexity to display the
varied types of data needed.  After trying Google Material Charts, I decided on plotly.js.  because it offered complex visualization 
capabilities with flexible trace layouts.  In order to overlay a treatment over symptoms, I needed to be able to have a second Y axis, 
otherwise the detail of the symptom tracking on a scale of 0-10 would be lost if I overlayed a medication that had a dosage of, for 
example 500mg.  I also chose to automatically graph new moon and full moon dates that coincided with the date range of a user’s data, 
because symptoms are often more intense a few days before or after those moon phases.  This allows users to account for that when 
assessing efficacy of treatment.  Full moons and new moons are represented with bubble traces, again highlighting the flexibility of 
joining various graph types in plotly’s api.

The other challenge was creating the data model, with enough generated fake user data to fully test and demo the functionality. Below is
a somewhat simplified representation of the data model.  I wrote several functions to generate fake user data in a way that mimicked the way
a real user might input data.

<img src="https://www.evernote.com/l/AMvT8CQQi4BGlJ4Ef7dRfB9cbRhDGVWd-g8B/image.png" alt="BEEtLyme_data_model" />

##Installation

Install PostgreSQL

To create and activate a virtual environment:

virtualenv env
source env/bin/activate

To install the project's dependencies:

pip install -r requirements.txt

##About Me:

BEEtLyme was created by Anna Liisa Moter.  She has been treating her own Lyme disease with Bee Venom Therapy for over 2 years, which 
inspired her to create this project.  She is a software engineer, mom, and all around nerdy polyglot living in Oakland, CA.

<a href="https://www.linkedin.com/in/anna-liisa-moter">Linked in</a>

<a href="https://github.com/annaliisamoter">Github</a>




