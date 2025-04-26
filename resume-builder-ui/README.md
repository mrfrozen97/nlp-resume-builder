# This UI is build upon OpenResume Resume Parser

## Instructions to Run

1. Install the dependency `npm install`
2. Start a development server `npm run dev`
3. Open your browser and visit [http://localhost:3000](http://localhost:3000) to see OpenResume live


## ➕ How to Add a New Page
- To add a new page, such as /about, follow these steps:​
- Create a New Folder: Inside src/app, create a new folder named about.​
- Add a page.tsx File: Within the about folder, create a file named page.tsx.​
- Define the Component: In page.tsx, define your React component. For example:

## 🔗 Adding the New Page to Navigation
- If you want to include a link to the new page in the site's navigation:​
- Locate the Navigation Component: src/TopNavBar.tsx and add your page to show in the topbar. Find the comment to add the page.