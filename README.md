# Bracketology Revamped
The new and improved version of the Beam Brackets Bracketology program.

## Example Workflow
In order to correctly use the codebase for Bracketology, the following workflow is desirable. The structure of the code is based on four classes: Team, Game, Conference, and Player. Data comes from multiple sources as well.
1. Gathering Data

    In order to do any statistical analysis or modeling, you will need to gather the data. This can be done using the functions in the fetch module. There are many functions, but the most important will fetch team stats, games, RPI rankings, and NET rankings. These four functions will gather the data and store it locally on your machine in a predetermined directory structure.
2. Creating the Objects

    The data will be wrangled into the corresponding classes mentioned previously. This is the most important and particular step in the codebase. The objects are codependant, so they must be created in a particular order. When creating teams, use the create_teams_from_stats function. This will use the stats you scraped to create the teams. Once created, you can use the methods in the Team class to store and create teams from a JSON file in the future. After the teams have been created, you can create the Conferences and Games. Conferences, like teams, are initially created using the stats, but can be created in future use through their JSON file. Games are created using the fetch_games function in the fetch module, and can also be created from their JSON file. Lastly, Players are created. Player code is currently in development.
3. Modeling and Analysis

    With your data loaded and objects created, you are ready to analyze and model college basketball statistics. Please use the JSON and data storage features to your advantage to avoid excess web scraping. The advantage of the class approach is through each class' search method, as well as all of the data being stored as attributes, custom data sheets and profiles can easily be created and their code is easily readable.