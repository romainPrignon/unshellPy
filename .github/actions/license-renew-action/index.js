const core = require('@actions/core')
const github = require('@actions/github')
const fs = require('fs')

const readLicenseFile = (licensePath) => {
    try {
        return fs.readFileSync(licensePath)
    } catch (err) {
        throw new Error('Failed to open license file')
    }

}

const incrementYear = (licenseContent) => {
    try {
        core.debug(licenseContent)

        const yearRegex = /\b(19|20)\d{2}\b/

        const newLicenseContent = licenseContent.replace(yearRegex, (year) => Number(year) + 1)
        core.debug(newLicenseContent)

        return newLicenseContent
    } catch (err) {
        throw new Error('Failed to open license file')
    }
}

const openPullRequest = async (githubToken, newLicenseContent) => {
    try {
        const octokit = new github.GitHub(githubToken)
        const context = github.context

        const { data: pullRequest } = await octokit.pulls.create({
            title: 'License renew action: License updated !',
            base: 'master',
            head: 'new-year-license',
            owner: 'License-bot',
            repo: context.repo.repo,
            body: newLicenseContent
        })

        return pullRequest.url
    } catch (err) {
        throw new Error('Failed to create a github pull request with new license content')
    }
}

async function run() {
    try {
        const githubToken = core.getInput('github-token')
        const licensePath = core.getInput('license-path')

        const licenseContent = readLicenseFile(licensePath)
        const newLicenseContent = incrementYear(licenseContent)
        await openPullRequest(githubToken, newLicenseContent)
    } catch (error) {
        core.setFailed(error.message)
    }
}

run()
