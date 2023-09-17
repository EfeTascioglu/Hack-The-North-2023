# Iridis | Hack The North 2023
Hack the North hosts a thousand hackers - and we can know them all by name. Iridis is a system combining AR, facial recognition, and other novel tech to bring our identities & stories into sight - literally. 

![original](https://github.com/EfeTascioglu/Hack-The-North-2023/assets/46626642/47ecc3ea-d64d-4a07-82ad-5a937aae8489)

![Watch a video demo here](https://youtu.be/dpprLOdzpI4)

## Inspiration
Iridis was born from three simple questions: "What's a problem that we'd really like to stop having?" "What tools and supplies can we use to fix this problem?" and, "How do we make that solution really damn cool?"

And, so, taking a page from the science fiction of the modern age and the hardware supplied to us by Hack the North, we've decided to bring together a proper smorgasbord of systems to build a way for us to meet (and remember!) our peers at a literal glance.

## What it does
Tony Stark would be proud of us. Our efforts and literal scrappiness has brought us a visor that can show us the names of hackers in our line-of-sight. (Scrappiness? Well, we probably collectively spent an hour digging through electronic scrap.). We use Adhawk glasses for eye-tracking and the ability to take pictures; we can snag images of our fellow hackers through blinking and winking, and feed those pictures through a RasPi to build a database of faces. How do we match faces to the names? Well, Hack the North has generously provided us a database of QR Codes that give us a wonderful, ethical-concern-free way to learn about and network with our peers.

Feeding back to the RasPi, we've custom-made a visor that displays names and biographical info in the front of your vision. Not only does it solve problems, but wearing it, you really feel like you're playing with something really awesome. We're envisioning a future where we can pre-load our tech with a database of event guests, allowing us to never awkwardly forget a name or connection ever again.
How we built it

At the end of things, we've got a metric truckload of interactions between our systems, all in service of bringing IDs to our Irises (get the name?). Our codebase is almost entirely in Python, as we prioritized ease of development and exploiting our collective familiarity with the language. The Adhawk API was at our frontend with the RasPi, with a Flask server operating on the backend, handling the heavy computing like data processing and face recognition. We used a hefty amount of computer vision with cv2, grabbing QR codes and faces from the built-in camera of the Adhawk glasses.

The visor was developed separately from the rest of the codebase, but depended upon very precise measurements and a hefty amount of verification with ray-tracing in order to settle the final geometry.

## Challenges we ran into
Overcoming the hurdles of development were absolutely not trivial. The Adhawk API, for instance, recently stopped supporting wireless camera output, whereas eye-tracker output only allows for wireless camera output. We also had to struggle with the computational cost of computer vision, simultaneously being forced to weigh our options for processors - between bluetooth-enabled systems without much processing, versus powerful devices without the ease of access of Bluetooth, further versus online systems. When we finally assembled our final prototype, we realized that the double reflections of the visor made our system too blurry. In the end, though, we always found workarounds, restoring morale and pushing us to challenge the limits of our ingenuity. If we wanted two outputs from the glasses, we would simply use two communication methods! Difficult decisions on computation had to be decided based on engineering metrics and constraints. And, if our visor's problem was material, then we would just need to find new materials through any means available, including digging up polarizing filters from the electronic waste bin. (Ultimately, applying a layer of permanent marker ended up mostly solving our problem.) Though this is a subset of the problems we've faced, it goes to show the length of consideration behind each and every attempt to make a difference in the world.
Accomplishments that we're proud of

Our breakthroughs are numerous, and worth celebrating. When asked, our members said:
- Though I've had several years of 3-D printing and CAD experience, the time pressure and size of the print in this event forced me to create my most precise CAD creation to date in the visor. Incorporating moving parts, crazy tolerances, organic forms, optics, and virtually zero ways to re-do if I messed up, I spent the entirety of the first night refining this thing. Perhaps it was luck, or perhaps it was a testament to my growth, but the visor worked first-try. - Andy
- Hard work doesn't always lead to success on the first try, but persistence can get you anywhere. Time and time again we ran headfirst into hurdles, obstacles, and broken passages. I don't think a single thing I did worked as initially visioned. But we persisted. Re-implemented. Found different solutions, with their own problems, each with their own solutions in turn. After a long struggle we found ourselves emerging from the other side battered and bruised, but still standing. Hack the North was a difficult journey, but I learned and grew a lot, and I stand refurbished on the other side. - Efe
- In the beginning of our design process, we wanted to use a feature of the Adhawk SDK that would tell us the location within the camera image that the user was looking at. However, it turns out that this feature was unavailable for HTN 2023. In spite of this, I was able to make use of my knowledge from my design teams and university experience to implement this feature myself, using OpenCV to find the camera's intrinsic and distortion matrices and projecting the points. I was even able to assist another Hacker with their project. This is just one of the many unexpected problems that we ran into; yet in spite of all these setbacks, our knowledge and passion pushed us all the way until the end, so we could make something as cool as Iridis. - Tyler
- I am proud about our OpenCV implementation on the Raspberry Pi. I was required to learn how to import packages on the device which was quite a unique experience and eventually the viewport actually working on the pie showed me a brand new system for my toolbox. - Sean

## What we learned
Challenges teach lessons for us, and given how many challenges we've had, it's only natural to feel like we're coming out of this feeling like different people. More serious lessons include ideas on optics, multithreaded data processing, and work delegation across well-organized and capable teams. Notably to us, fast-paced environments such as this one teach exceptional lessons on improvisation, and moving forwards even when being hounded by obstacles. Though it's a lesson in finding stability in the "good enough", it's also a lesson in searching out avenues of constant progress, even in the face of imperfections. Perhaps, in a society plagued by such imperfections, experiences such as Hackathons serve as more profound metaphors than we may normally believe?

## What's next for Iridis
Iridis is simply a functional idea, that we tried to build in a cool way. Our experiences have motivated further learning in various aspects of tech dev, and we're more than happy to simply have brought our vision to reality for the time being. However, we've also got a heck of a lot of ideas to make Iridis better, and potentially to expand the system to being a more generally applicable one beyond just Hack the North's ecosystem. What happens next is ultimately not clear, but we're very happy with the way things have gone until now. If anyone is interested in the process, build, or ideas, we'd be ecstatic to chat!

For more information, check out the devpost ![here](https://devpost.com/software/iridis)

## Working Docs
### API Endpoints
- First Left Blink -> QRDETECT Signal. Search for QR Code and scrape website for user data.
    - Store the name and information in a database (?)
    - Returns all of the data in a variable called name_and_data, with the name and data separated by a newline
- Second Left Blink -> FACEDETECT Signal. Add face to database. 
    - POST api.efetascioglu.com/api/add_face.  data: {"image": base64 encoded image, "eye_pos": (x, y), "name_and_data": name and data (separated by a newline)}
    - Returns: {"success": true/false}
- Right Blink -> RECALL Signal. Search for face in database
    - POST api.efetascioglu.com/api/search_face.  data: {"image": base64 encoded image, "eye_pos": (x, y)}
    - Returns: {"success": true/false, "name_and_data": name and data (separated by a newline)}
