# Github Archiver

Github Archiver is a project that was inspired by the [DMCA warning and removal](https://github.blog/2020-11-16-standing-up-for-developers-youtube-dl-is-back/) of youtube-dl.

While Github did the right thing here, it makes you wonder, how many other idiotic laws will remove a meaningful project from the community. 

So I made this for myself, and I thought I share it out. This is not meant to be a library that is used outside its docker container. You can if you wish.

The script relies on environment variables to initiate its jobs. 

- `GITHUBARCHIVER_AT`: Your Github Access Token to prevent rate limiting and access to private repos
- `GITHUBARCHIVER_ORGS`: The oginizations (or users) you want to clone. e.g. `signalapp` 
- `GITHUBARCHIVER_REPO`: If you didn't want to clone everything under an orginization or a user, you can clone specific projects. e.g. `joubin/GithubArchiver`
- `GITHUBARCHIVER_RUNDAILY`: If set to `true`, it will run daily at 1am. 





