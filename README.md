# NATIVE DISC GOLF - A disc golf retail website
#### Video Demo:  <https://youtu.be/LRg7utIq12E>
#### Description:
##### Introduction
For my final project, I chose to make an example disc golf retail website.
Many of the current disc golf retailers' websites are not that great and all seem to have some things that they could be doing better.
Many of them feel cluttered, some feel slow, and some just look downright ugly.
So, I figured that with my new coding skills learned from CS50, I could try and create a retail website for disc golf that looks and feels better than any of the current ones.
The name "Native Disc Golf" is simply a placeholder name for a fake retailer that I came up with.

##### Database
To simulate a retail inventory, I created a sqlite database called **inventory.db**.
This database contains a simple table that includes information about every product this retailer has in stock.
For discs, that includes the following columns:
- id (PRIMARY KEY)
- brand
- mold
- plastic
- run
- weight
- type
- speed
- glide
- turn
- fade
- price
- image

To make my life a little bit easier, I created a csv file from google sheets with a plethora of products that I could use.
I then made a python program called **import.py** that would read the information from this csv file and import it straight into my database.
This just served to make the database population a little bit easier.

##### Templates
All of the html templates are stored in the /templates folder.
I am using a **layout.html** file to keep the header and footer the same on every page.
Using jinja, I can copy this same layout into every other html template on the site.

##### Static
This folder contains all of my unchanging files like images, this **README.md**, as well as my javascript and css files.
For my webpage styling, I'm using a lot of the default bootstrap styles, layouts, and grids, with some tweaking here and there when I felt it was necessary.

##### Home Page
In **app.py**, I am using the flask framework to render all of my html templates and retrieve all of the database information.
On the home page, **index.html**, for new releases the program searches for the 24 most recently added disc runs and then displays them each in a bootstrap card using a jinja for loop.
The card includes the disc's image, brand, plastic, mold, and run.
CSS styling is used to make a hover effect that displays all of this information on mouse hover.
This makes the site feel more fluid and interactive, which is something that other disc golf retail websites are lacking.
The user can then click on this image and be taken directly to that specific mold's item description page.
The same is done for each of the following apparel and accessories sections.

###### Navigation
The top header navigation bar is a bootstrap navbar with some personal styling added.
The leftmost title serves as a redirect link back to the home page.
The middle sections serve as quick searches where the user can search for items by type or brand.
The far right contains the search bar and a quick link to the user's shopping cart.
The navbar is fixed to the top for better UX, allowing the user to scroll and peruse the site while still being able to search or access their cart easily at any time.

###### Search Bar
The search bar is fully functioning, allowing for searches of any keyword relating to mold, brand, type, run, etc.
This is done using a SQL query in **app.py** that selects any inventory items similar to the search.
Every distinct item is displayed in another list of cards containing the item's image, name, and flight numbers (if applicable).

###### Search By Flight
For this section, the program starts by reading every unique disc mold currently in inventory.
I render each of those discs onto the home page but also hide them from view.
Once a value on any of the range sliders is changed, there is a javascript function that shrinks the form section, and then searches for and displays the first 6 molds currently in inventory with values that match the search.
There is also another javascript function that controls how the results on the right fade in, making the site feel a little more smooth and responsive.
The "Find More >" button redirects to the search page with a specific SQL query with the values given in the form.
This is intended for when there are more than 6 results in inventory (which there most likely would be for an actual retailer with thousands upon thousands of discs).
In theory, this is to make it easier to find discs by their flight characteristics.
Many people come looking for discs similar to one they already own, and so using this form would be a great way for them to find molds from other brands that have the same flight characteristics.

###### Team Profiles
This is a simple section displaying information on all of this retailer's sponsored players.
The user can scroll through these and get a quick profile on each player.
This data is currently inputted straight into the html file and is not accessed through the database, although that may very easily be done.

###### Footer
The footer is just the last section of **layout.html** that includes some basic information as well as links to socials and important documentation.
The socials are currently linked to the homepage of each site as this retailer does not actually exist.

##### Item Page
Every distinct item or mold has its own description page that gives info on the disc as well as lists every individual item of that type currently in stock.
This is again done using a SQL query in **app.py** that selects all individual inventory items of that mold.
Ideally, each individual item would have its own specific photo, allowing the user to see exactly what they are getting.
However, as this is just a template, the same default images for each mold are used in place of individual images.
Once the items are selected from the database, they are displayed in a list of bootstrap cards similar to the home page, just adding borders for readability in addition to some extra information and an "Add to Cart" button.
The user can sort all of these individual items by plastic and then further again by run.
The plastic dropdown is populated through a SQL query that looks for all distinct plastic types of this mold.
When a plastic is selected, the run dropdown is then populated with all runs of this specific mold in this specific plastic.
For example, if there were two runs of Innova Firebirds in Glow Champion plastic, a 2021 Nate Sexton Tour Series and a 2022 Nate Sexton Tour Series, the run section would be populated with these two runs only once the user selects the Glow Champion plastic in the plastic dropdown.
The user can go back to looking at every disc by simply re-selecting the "All Plastic" option in the dropdown.

##### Cart
The cart can be accessed at any time by clicking the shopping bag icon on the far right side of the navbar.
When the "Add to Cart" button for any item is clicked, the user is automatically redirected to their cart to see what is currently in it.
The user's shopping cart is tracked using a flask session variable so that it is saved even after the browser window is exited.
The cart page adds the prices of each item currently in the cart to display the total in the "Checkout" button at the bottom of the page.
The user can also remove any unwanted items at any time by clicking that item's "Remove" button.
This then tells the program to remove that specific item from the current session's cart variable in **app.py**.
Once the user clicks "Checkout," they are redirected to the home page with an alert message telling them that their order is on its way.
In an actual ecommerce website, of course the checking out would include entering of card info, shipping address, and other information, but I figured that this would be enough for now just to simply display the site's functionality.

##### Responsive
The website is fully responsive on every page, allowing for ease of use on any device.
The item lists shrink down and display less on each row whenever necessary, and the navbar collapses using a bootstrap template.
On smaller screens, when the navbar collpases the shopping cart link is moved to the bottom left of the screen and, thanks to a javascript function, only appears when the collapsed navbar is expanded.
This keeps the navbar looking clean while keeping the cart icon out of the way while not in use.
