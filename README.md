# An (un)official Game Forum
A web app in Django that is meant to resemble classic game forums, with threads, comment sections, re-post functionalities and more. Share your thoughts over the game, your achievements, and find a community!<sub>_Game does not exist and does not come with the web app_</sub> 

-> [Try it yourself!](https://web-production-b59ae.up.railway.app/ "Game Forum Project") <-


## Features Overview

* **User Profiles**

  * Create your own profile.
  * See all that you posted and how it's doing in a feed inside the profile.

* **Follow Requests**

  * Send follow requests through user profiles.
  * Manage pending requests in your inbox.

* **Posts**

  * Create new posts with text or images.
  * Like and share content or comments posted by others.
  * Comment on posts to engage in discussions.
 
* **Share-post functionality**

  * Do you feel like your response to a thread deserves a post on its own? You can share any post inside the platform itself.
  * Add captions, or images to your shared threads.
 
* **For You Feed**

  * Displays recommended topics and trending discussions, or recently viewed threads to continue your discussion.

* **Topic Tag**

  * Customized tags for each thread, that help build your for-you feed.
 
* **Inbox**

  * A simple notification engine, that will alert you when another user interacts with your post, shares it, or sends you a request.

* **Flexible Log-in**
  * Forgot your username? You can also log-in through the mail you registered during the user creation.

* **Moderator role**
  * Normally, a user can't edit nor delete any post that isn't theirs. A moderator can, and not just the posts: the comments as well--whenever a comment is deleted by a moderator because it breaks any of the rules, the app will show a tag that indicates it.
  * If a moderator chooses to, they can ban a user, or un-ban them.     
     
<hr>
## Quick User Guide
To register as a new user, simply click over the Sign up button to the right side of your main feed, or through the sign-up option in the log-in interface. Once you've registered successfully (mind that duplicate emails aren't allowed), you'll be able to access your profile from the navbar of the site, where you'll also see your profile picture, date of creation, number of followers, and your own posts to the right. Through the same navbar I mentioned, you can also create new posts, and check your inbox. Inside any post you can leave comments and like both comments and the post itself. Through the share button, either inside every post, or through the three-dot icon on the right, you'll be able to re-post any thread with a personalized caption, or even a reaction image. To send requests to other users, simply head to their profile, by clicking their name on the posts, or home feed, and send the request from there--you'll get a notification, if and when your pending request has been accepted by the other user.


## Code Structure Overview

  * Structured in two main apps:
    * **Base**
       * Manages everything related to the posts and re-posts, comments, likes and feeds.
    * **Usermanager**
       * As the name implies, this app contains everything related to the user themselves, the log-in/outs, registrations, profile and the notification system.
  * Hosted on Railway, Built with Django framework, Whitenoise, PostgresDB and image hosting is done through Cloudinary-- more in-depth requirements for downloading the project and running locally are listed inside the [requirements file](https://github.com/qvnn025/Social-ppm/blob/master/requirements.txt "requirements") , [here](https://github.com/qvnn025/Social-ppm/tree/adm) for the rest.



## Disclaimer

This is a University project, and everything used inside the app is done for educational purposes. In light of that, everything written in the posts, or shared by users isn't representative of, or a responsability of, my university or myself.




   > [!CAUTION]
>Do NOT use any real email or password in the user registration.
