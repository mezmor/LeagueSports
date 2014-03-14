LeagueSports
==============
The Fantasy League of Legends Portal/Manager


User-user interaction
----------------------
Users should be able to sign up to the website
    * unique username, unique email
    * email verification to complete account registration

Users should be able to add users to their friends list + ignore list
    * no confirmation required, akin to a 'watching' list
    * ignore list disallows any messages (block trades? warn when in the same league?)

Users should be able to send messages to other users
    * ignore list prevents message from being received

Users should be able to see a list of all other users (LIST VIEW)
Users should be able to see details about the other users (DETAIL VIEW)
    * what leagues they are in
    * what leagues they are commishing
    * win/loss record, trade history
    * join date
    
User-league interaction
----------------------
#### User-league management behavior

Users should be able to join a league
    * If the league is private they may send a join request
    * If the league is public they may simply join it
    * Commish may invite users to join the league
        * Extension: users can invite other users
            * If the league is public the invited user simply joins
            * If the league is private, the invited user sends a join request to the commish
    * The user may join a league via:
        * Button on All Leagues list
        * Button on User's League list
        * Button in League detail

Users should be able to leave a league
    * their team is disbanded and all players become free agents
    
Users should be able to create a league
    * league properties to set on creation (creation form):
        * name
        * size: min 2, max 32
        * public/private
    
Users should be able to see a list of all leagues (LIST VIEW)
    * league name, size, commish, privacy setting (private = must be accepted/invited to join)
    
Users should be able to see details about leagues (DETAIL VIEW)
    * Selector tabs: Standings, Rosters, Scoring, Playoffs, Draft, My Team
        
    
#### Internal user-league interaction

Commish should be able to alter league settings:
    * Commish
    * Name
    * Size 
        * Suggested: 8 or 10 players
    * Draft date/time (all player-management is locked until then)
    * Line-up locks: Daily/Weekly
    * Max. trades per team per day/week
    * Region selection (NA/EU)
        * Notify if num. of LCS players <= num. of available player slots in the league
    * Team size (min 5.)
        * Suggested: One player per role, one or two subs
    * Score calculation
        * Broken down per role
        * User defined, uses variables of the player to form an equation
            * Provides example ranges
            * [variable] syntax, variables: kda, cs, gold, game time
            * Suggested numbers:
                * Top/Mid/ADC: ([kda] * 15 + [cs]) / [game time]
                * Jungle: ([kda] * 25 + [cs]) / [game time]
                * Support: ([kda] + [gold]) * 25 / [game time]
        * Bonuses/penalties for special occurences
            * same syntax as score, but with conditionals
            * Suggested settings:
                * +20% of score for 0 deaths AND 10+ kda
                * -20% of score for losing
    * Enable/disable playoff bracket
        * Play the first 8 week schedule normally, then play 3 weeks of single-elimination bracket (DEFAULT)
        * Play the full 11 week schedule normally


        
When users join a league, they automatically create a default FantasyTeam within a league that they interact with
* FantasyTeam settings:
    * Name
    * Avatar/picture
    * Players
        * Add/drop players
        * Propose trades
        * Swap players (active/sub)
    * COMMISH-ONLY SETTINGS:
        * Draft pick order
    

Match-up interactions
----------------------
Users should be able to view every week's match-up, i.e. the league's schedule
    * Users should be able to edit their team in the match-up view
    * Each match-up view should display:
        * Team's current line-up/score
    

Draft interactions
----------------------
Users should be able to see the draft order prior to the draft beginning
    * season#, round#, pick#, team
Users should be able to see the draft order with picks after the draft has ended
    * season#, round#, pick#, team, player pick
Users should be able to join the draft after it has begun, but not after it has completed
Users should be able to see the time until the draft starts/if it is under way

Refactoring brainstorm
=======================
Views (the controllers) often have logic checks on whether or not it should execute code.
Examples of this are the @login_required decorator, or to check if a requesting user is the owner of a team: "if request.user == team.manager:".
These checks are in place in case someone accesses the view via its URL directly by typing for example: "leagues/<league_id>/del/<user_id>" with some existing IDs in their browser.
However, the main flow of accessing a URL is via an anchor that we expose to the user for GETs or a form action for POSTs.
When we expose these URLs in templates we only want to expose them to a subset of the users accessing the page.
For example, on any team detail page, the team manager should have the ability to leave the league via a form action.
For this reason we also have the same logic checks in the template as we do in the view.
This kind of pattern goes against the DRY nature of python/django, unless we are smart about where we write our access logic.
Solution suggestion: the view contains a method that checks user access, and we pass this method to the template to utilize the same check

Detail view completion 
=======================
As far as displaying the right content is concerned.

- [ ] Users
    - [x] new.html
    - [ ] user.html
    - [ ] users.html
    
- [ ] League
    - [x] leagues.html
    - [x] new.html
    - [ ] draft.html
    - [ ] playoffs.html
    - [x] rosters.html
    - [ ] schedule.html
    - [x] scoring.html
    - [x] standings.html
    
- [x] Settings (Commish Panel)
    - [x] requests.html
    - [x] settings.html
    
- [ ]  Team
    - [ ] picks.html
    - [ ] roster.html
    - [ ] schedule.html
    - [ ] transactions.html
    - [ ] settings.html