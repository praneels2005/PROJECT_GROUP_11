CSC 315 - Project 11
Bryan Wieschenberg, Tra-Mi Cao, Praneel Pothukanuri

This database holds information of goats, along with their traits and activities. In our project, we aim to answer 7 questions about goats and their birth weights using our views and queries, enabling the user to choose a variety of years, vaccines, and outputs for each question answered. The 7 questions are:

1. Birth weight comparisons for each year the data is available.
2. Lowest average, median average, high average and overall average.
3. The average age of the does that gave birth that year.
4. Average wt. of twins, triplets and singles – comparison.
5. Birth weight differences between first year moms and older moms.
6. Kid number differences between first time moms and older moms.
7. Dam vaccines' effect on their kids' birth weight.

Here is how to create and populate our database and for it to be used in the graphic user interface:

1. Create a database in within a PostgreSQL terminal using the command 'createdb Group11DB'
3. Make sure all files are downloaded and all located in one central directory, as well as the 5 data files
4. Ensure you're in the correct directory where all the files are located, navigating with 'cd {directory}' and 'ls' to see the contents of that directory to make sure you're correctly located
2. Go into the database using the command 'psql Group11DB'
5. Use the command '\i schema.sql' to create our schema's tables and populate them.
5. Using our views.sql file, copy and paste every view into the database to create each view necessary for the GUI
6. Once all views are created, you may exit the database using '\q'
7. Out of the database, type into the terminal 'flask run', you should receive a message saying the Flask app is running
8. Go into a browser and type at the top the link 'localhost:5000'
9. You have now loaded the Flask app and are able to fetch and display database queries in the GUI. Congratulaions!
