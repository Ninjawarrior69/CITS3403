# Reading Tracker User Stories

## US-01: Browse Shared Library

As a reader, I want to browse a shared library of books so that I can discover what others are reading.

Acceptance criteria:

- User can view a list of books in the shared library.
- Each book card shows basic details (title, author, and average star rating).
- User can open a book detail page from the library list.

## US-02: Rate Books With Stars

As a reader, I want to rate a book with stars so that I can express my opinion and help others choose books.

Acceptance criteria:

- User can submit a star rating (for example, 1 to 5 stars) for a book.
- The system updates and displays the average star rating.
- User can update their own rating, and only their latest rating is counted.

## US-03: Comment on Books and View Community Feedback

As a reader, I want to comment on books and read comments from other users so that I can discuss and evaluate books together.

Acceptance criteria:

- User can post a comment on a book.
- Comments show the author username and timestamp.
- All users can view comments on the book detail page.

## US-04: Create a Personal Reading List

As a reader, I want to save books to my personal reading list so that I can keep track of books I want to read or am currently reading.

Acceptance criteria:

- User can add a book to their personal reading list.
- User can remove a book from their personal reading list.
- The reading list is visible from the user’s account or profile page.

## US-05: Search for Books

As a reader, I want to search for books by title or author so that I can quickly find books I am interested in.

Acceptance criteria:

- User can enter a keyword into a search bar.
- The system returns books with matching titles or authors.
- User can open a book detail page from the search results.

## US-06: Explore the Website Without Logging In

As a visitor, I want to explore the website without logging in so that I can understand its purpose and features before creating an account.

Acceptance criteria:

- Visitor can access public pages such as the home page and shared library without logging in.
- Visitor can view basic book information and community content that is publicly available.
- Visitor can clearly see options to sign up or log in when they want to interact with the website.

## US-07: Create an Account and Log In

As a new user, I want to create an account and log in so that I can save my reading activity and interact with the community.

Acceptance criteria:

- User can register with a username, email, and password.
- User can log in with valid account details.
- After logging in, the user can access features that require an account, such as rating and commenting.

## US-08: Follow Other Users

As a user, I want to be able to follow other users so that I can easily view my friends and favourite users profiles. 

Acceptance criteria:

- User can follow other users through their profile.
- User can view following list to easily access these accounts.
- Follower and following count is displayed on profile page. 

## US-09: Edit Profile

As a user, I want to be able to edit my profile at any time so that I can keep it up to date. 

Acceptance criteria: 

- User can change edit features such as name, email, bio, picture. 
- User can change which favourite books are displayed on their profile.
- User can delete reviews associated with their profile. 

## US-10: View Reading Statistics

As a user, I want to be able to view statistics for each of my bookshelves. 

Acceptance criteria:

- Number of books in Read, Currently Reading, To Be Read, Did Not Finish shelves displayed on profile.
- Users can click on these sections to access full list of books.
- Number will update as books are added and removed from shelves.

## US-11: Display Favourite Books on Profile

As a user, I want to be able to display my favourite books on my profile to show current interests. 

Acceptance criteria:

- User can add top 6 favourite books to profile.
- Books will be under Favourite Books section header.
- Can be edited at any time to reflect current favourites.

## US-12: Track Reading Progress

As a user, I want to be able to keep track of what page I am up to for books I am currently reading. 

Acceptance criteria:

- Progress bar is displayed for currently reading books.
- Page number can be entered to track progress.
- Book length will be retrieved from API to calculate progress percentage. 