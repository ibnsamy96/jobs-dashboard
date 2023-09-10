const axios = require("axios")
const cheerio = require("cheerio")

function generateSearchPageLink(pageNum, query) {
	const queryLink = `https://wuzzuf.net/search/jobs/?filters%5Bpost_date%5D%5B0%5D=within_1_week&q=${query}&start=${pageNum}`
	return queryLink
}

function findIsLastPage(jobsArray) {
	return jobsArray.length <= 0
}

async function fetchPageHtml(url) {
	try {
		const response = await axios.get(url)
		return response.data
	} catch (error) {
		throw error
	}
}

function createJobObject(kwargs) {
	const job = {
		title: kwargs.title,
		description: kwargs.description,
		href: kwargs.href,
		location: {
			city: kwargs.locationCity,
			country: kwargs.locationCountry,
		},
		company: {
			name: kwargs.companyTitle,
			logo: kwargs.companyImage,
			url: kwargs.companyWebsite,
		},
	}
	return job
}

function parseJobTitle(jobDiv) {
	return jobDiv.find("h2 a").text().trim()
}

function parseJobDescription(htmlCodeParser, jobDiv) {
	const fullDescription = []
	const headlines = jobDiv.find(".css-1lh32fc a")

	headlines.each((index, element) => {
		fullDescription.push(htmlCodeParser(element).text())
	})

	const generalInfo = jobDiv.find(".css-1lh32fc").next().text().trim()

	fullDescription.push(generalInfo)

	return fullDescription.join(" · ")
}

function parseJobHref(jobDiv) {
	const jobRelativeHref = jobDiv.find("h2 a").attr("href")
	const jobAbsoluteHref = `https://wuzzuf.net${jobRelativeHref.split("?")[0]}`
	return jobAbsoluteHref
}

function parseLocationCityAndCountry(jobDiv) {
	const location = jobDiv.find(".css-d7j1kk span").text()
	const locationParts = location.split(",").map(part => part.trim())
	const locationCountry = locationParts.pop()
	const locationCity = locationParts.pop()
	return { locationCity, locationCountry }
}

function parseCompanyTitle(jobDiv) {
	return jobDiv.find(".css-d7j1kk a").text().slice(0, -1).trim()
}

function parseCompanyWebsite(jobDiv) {
	return jobDiv.find(".css-d7j1kk a").attr("href")
}

async function fetchAndParsePageJobs(pageNum, query) {
	const pageJobs = []
	const pageLink = generateSearchPageLink(pageNum, query)
	console.log(pageLink)
	const pageHtml = await fetchPageHtml(pageLink)
	const $ = cheerio.load(pageHtml)
	const jobDivs = $("div.css-pkv5jc")

	jobDivs.each((index, element) => {
		const jobDiv = $(element)
		const title = parseJobTitle(jobDiv)
		const description = parseJobDescription($, jobDiv)
		const href = parseJobHref(jobDiv)
		const { locationCity, locationCountry } =
			parseLocationCityAndCountry(jobDiv)
		const companyTitle = parseCompanyTitle(jobDiv)
		const companyWebsite = parseCompanyWebsite(jobDiv)

		const jobInfo = createJobObject({
			title,
			href,
			description,
			companyWebsite,
			companyTitle,
			locationCity,
			locationCountry,
		})

		pageJobs.push(jobInfo)
	})

	return pageJobs
}

async function getAndConcatenateData(query) {
	const allJobs = []
	let pageNum = 0
	const maximumNumOfPages = 10 // maximum number of pages to search in
	let jobsCount = 0

	const start = Date.now()

	while (pageNum < maximumNumOfPages) {
		const pageJobs = await fetchAndParsePageJobs(pageNum, query)
		const isLastPage = findIsLastPage(pageJobs)

		const now = Date.now()
		const elapsedTime = now - start

		if (elapsedTime > 8000 || isLastPage) {
			console.log(elapsedTime)
			break
		}

		jobsCount += pageJobs.length
		allJobs.push(...pageJobs)

		pageNum++
	}

	return [jobsCount, allJobs]
}

async function getJobs(query) {
	const [jobsCount, allJobs] = await getAndConcatenateData(query)
	const jobsObject = { type: "wuzzuf", count: jobsCount, results: allJobs }
	return jobsObject
}

// Example usage:
const query = "frontend"
getJobs(query)
	.then(jobs => {
		console.log(jobs)
	})
	.catch(error => {
		console.error("Error:", error)
	})
