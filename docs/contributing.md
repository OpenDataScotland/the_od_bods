# Never used git/github before?
More help at the bottom of this page!


# Super-quick contributor guide

1. Get [issue](https://github.com/OpenDataScotland/the_od_bods/issues): Find the issue you're working on OR create a new one.

2. Create branch from issue:
    - In issue webpage, on right-hand bar of issue, scroll to the _Development_ section and click _Create a branch_.
    - Fetch and checkout to new branch

3. Make changes in branch    
    - Add and commit changes
    - Push to branch

4. Create pull request
    - Resolve merge conflicts (if any)
    - Let tests run, resolve issues if any
    - Request a reviewer (optional: somebody will pick it up but if you have had prior discussions with a repo admin it may be good to request their review.)
 
 5. Wait
    - Reviewer will review/request changes/ merge PR
    - Reviewer to merge and delete branch
    

6. Enjoy that contributor feeling!


# More detailed contributor guide
Thanks to @gavbarnett for writing this section
1. Fork this project

    This will create a clone of the project into your personal online GitHub account.

    Normally you should fork from the head of 'main' unless you're purposefully contribution to an existing branch.


2. Create a branch on your fork of the project immediately.

    Name the branch based on the feature/fix you are about to add (branch naming format? "BR_Fancy-new-feature"). Each branch should try to add only one logical feature/fix. If you want to do multiple things then make a separate branch for each.

    This means when you later issue a pull request (PR) from this branch and you are asked to make changes these are all inside a branch. This allows you to work on multiple features and PRs in parallel without conflicts.


3. Make your changes in the branch

    Often this will be over multiple commits.

    Try to make each commit do just one (normally fairly small) logical thing. And describe why you've made the change in the commit message. (What you've changed is clear by the code, but why is often not so clear.) Also in your commit message should be any testing you performed/ or did not perform.


4. Issue PR or Draft PR

    First ensure your project fork/branch is up to date with this repo. Do this by updating your 'main' branch from 'upstream remote' then update your feature branch from 'main'. This keeps your 'main' aligned with ours.(I need to check that's correct).

    Check your code still works as before then do either:

    A) If you have completed the feature/fix and think your code is ready for inclusion in the original project raise a PR from your branch to this repo. Your code will be reviewed before being accepted, you may receive a request for changes.

    B) If you would like a review, guidance, or help completing a feature/fix you can instead issue a Draft PR from your branch to this project.



### Need more guidance?
This [repo](https://github.com/firstcontributions/first-contributions) walks through the process for forking, branching, and submitting PRs, or contact one of the team on [Slack: Open Data Scotland](https://join.slack.com/t/opendatascotland/shared_invite/zt-yfcc64tg-xIF1cOxkWbKZqI8ZBPzkGg) #ods-website