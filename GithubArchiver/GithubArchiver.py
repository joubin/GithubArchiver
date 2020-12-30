from github import Github
from github.GithubException import UnknownObjectException

import logging
import os
import shutil
import git
from git.exc import InvalidGitRepositoryError, GitCommandError


class GithubArchiver:
    GITHUBARCHIVER_AT: str = "GITHUBARCHIVER_AT"
    GITHUBARCHIVER_USER: str = "GITHUBARCHIVER_USER"
    GITHUBARCHIVER_PASSWORD: str = "GITHUBARCHIVER_PASSWORD"
    ROOT_WD = os.getcwd()
    logging.basicConfig(format='%(levelname)s | %(asctime)s | %(message)s', level=logging.INFO, datefmt='%m/%d/%Y '
                                                                                                    '%I:%M:%S %p')

    def __init__(self):
        self.github: Github = self.authenticate()
        command = f"git config --global url.\"https://{os.getenv(GithubArchiver.GITHUBARCHIVER_AT)}:@github.com/\".insteadOf \"https://github.com/\""
        os.popen(cmd=command).read()

    def authenticate(self) -> Github:
        if os.getenv(GithubArchiver.GITHUBARCHIVER_AT) is not None:
            return GithubArchiver.authenticate_token()
        elif os.getenv(GithubArchiver.GITHUBARCHIVER_USER) is not None and os.getenv(
                GithubArchiver.GITHUBARCHIVER_PASSWORD) is not None:
            return GithubArchiver.authenticate_userpass()
        else:
            raise ValueError(f"Set {GithubArchiver.GITHUBARCHIVER_AT} with your token as your environmental variable.")

    @staticmethod
    def authenticate_userpass() -> Github:
        raise NotImplemented("Authenticating with username and password has some sharp edges, for that reason, "
                             "this is not implemented. See https://docs.github.com/en/free-pro-team@latest/github"
                             "/authenticating-to-github/creating-a-personal-access-token")

    @staticmethod
    def authenticate_token() -> Github:
        return Github(os.getenv(GithubArchiver.GITHUBARCHIVER_AT))

    def download_by_repo(self, repo_name: str):
        os.chdir(GithubArchiver.ROOT_WD)  # Go to the root working direcotry
        try:
            repo = self.github.get_repo(repo_name)
        except UnknownObjectException:
            logging.error("Could not find a repo {repo}. Please ensure full path e.g joubin/GithubArchiver".format(
                repo=repo_name))
            return
        try:
            GithubArchiver.__clone(repo.clone_url, repo_name=repo.name, parent_name=repo.parent.name)
        except FileExistsError:
            GithubArchiver.__pull(repo_path=repo.name, parent_name=repo.parent.name)

    def download_by_org(self, org_name: str):
        os.chdir(GithubArchiver.ROOT_WD)  # Go to the root working direcotry
        try:
            org = self.github.get_organization(login=org_name)
        except UnknownObjectException:
            logging.debug("Org is a user, attempting to get user")
            org = self.github.get_user(login=org_name)

        if not os.path.exists(org.login):
            os.makedirs(org.login)
        else:
            logging.info(f"A folder for {org_name} already exists. Will iterate repos.")

        os.chdir(org.login)
        repos = org.get_repos()
        for repo in repos:
            if not os.path.exists(repo.name):
                GithubArchiver.__clone(clone_url=repo.clone_url, repo_name=repo.name, parent_name=repo.owner.login)
            else:
                GithubArchiver.__pull(repo_path=repo.name, parent_name=repo.owner.login)

    @staticmethod
    def __clone(clone_url, repo_name, parent_name):
        os.chdir(GithubArchiver.ROOT_WD)
        if not os.path.exists(parent_name):
            os.makedirs(parent_name)
        os.chdir(parent_name)
        if not os.path.exists(repo_name):
            git.Repo.clone_from(url=clone_url, to_path=repo_name)
            logging.info("Finished cloning {repo_name}".format(repo_name=repo_name))
        else:
            logging.error(f"Folder {repo_name} already exists.")
            raise FileExistsError

    @staticmethod
    def __pull(repo_path: str, parent_name: str):
        os.chdir(GithubArchiver.ROOT_WD)
        if not os.path.exists(parent_name):
            logging.error(f"{parent_name} does not exist.")
            raise FileNotFoundError
        os.chdir(parent_name)
        try:
            if os.path.exists(path=repo_path):
                git.Repo(path=repo_path).remote().pull()
                logging.info(f"Finished pulling {repo_path}")
            else:
                logging.error(f"The path {repo_path} was not found")
        except InvalidGitRepositoryError:

            logging.error(f"The specified folder \"{repo_path}\" is not a git directory. Deleting the potentially "
                          f"broken file. Will address the issue on the next run")
            shutil.rmtree(path=repo_path)
        except GitCommandError:
            logging.error(f"The specified folder \"{repo_path}\" is a git directory, but its causing the git command "
                          f"to have issues. Deleting the potentially broken folder. Will address the issue on the "
                          f"next run")
            shutil.rmtree(path=repo_path)
def run_main():

    logging.info("Getting Orgs and Users")
    archiver = GithubArchiver()
    if os.getenv("GITHUBARCHIVER_ORGS") is not None and os.getenv("GITHUBARCHIVER_ORGS") != "":
        for org in os.getenv("GITHUBARCHIVER_ORGS").split(","):
            logging.info(f"Working on {org}")
            archiver.download_by_org(org_name=org)
    else:
        logging.info(
            "Did not find any environmental variables for GITHUBARCHIVER_ORGS. If you want to clone entire users or "
            "orgs, set the variable to a comma separated list")

    logging.info("Getting Individual Repos")

    if os.getenv("GITHUBARCHIVER_REPO") is not None and os.getenv("GITHUBARCHIVER_REPO") != "":
        for repo in os.getenv("GITHUBARCHIVER_REPO").split(","):
            logging.info(f"Working on {repo}")

            archiver.download_by_repo(repo_name=repo)
    else:
        logging.info(
            "Did not find any environmental variables for GITHUBARCHIVER_REPO. If you want to clone entire users or "
            "orgs, set the variable to a comma separated list")
