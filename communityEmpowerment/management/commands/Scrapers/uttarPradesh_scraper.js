const puppeteer = require('puppeteer')
const fs = require('fs')
const { v4: uuidv4 } = require('uuid');

async function departmentUrls(){
  browser = await puppeteer.launch()
  page = await browser.newPage()
  await page.goto("https://www.yuvasathi.in/home/#gss")
  const result  = await page.evaluate(()=>{
    const department_urls = document.querySelectorAll(".facts .row a")
    const departmentUrlList = []
    department_urls.forEach((node)=>{
      const departmentUrl = node.href
      departmentUrlList.push(departmentUrl)
    })
    return departmentUrlList
  })
  await browser.close()
  return result
  
}


async function schemeUrls(){
  const departmentUrlList = await departmentUrls()
  browser = await puppeteer.launch()
  page = await browser.newPage()
  const allSchemeUrlList = []
  for (const departmentUrl of departmentUrlList){
    await page.goto(departmentUrl)
    const paginationUrlList = []
    let { schemeUrls, paginationUrls } = await page.evaluate(() => {
        const paginationNodes = document.querySelectorAll(".pagination li:not(:first-child):not(:last-child)");
        const paginationUrlList = [];
        paginationNodes.forEach(node => {
          const linkElement = node.querySelector('a');
          if (linkElement) {
            paginationUrlList.push(linkElement.href);
          }
        });
      const schemeUrlNodes = document.querySelectorAll(".container .col-md-9 .row:not(:nth-child(1)):not(:nth-child(2))")
      const schemeUrlList = []
      schemeUrlNodes.forEach((node)=>{
        const schemeUrl = node.querySelector('a').href
        schemeUrlList.push(schemeUrl)
      })
      return { schemeUrls: schemeUrlList, paginationUrls: paginationUrlList }
    })
    allSchemeUrlList.push(...schemeUrls)

    for (const pageUrl of paginationUrls) {
        await page.goto(pageUrl, { waitUntil: 'load', timeout: 0 });
  
        const moreSchemeUrls = await page.evaluate(() => {
          const schemeUrlNodes = document.querySelectorAll(".container .col-md-9 .row:not(:nth-child(1)):not(:nth-child(2))");
          const schemeUrlList = [];
          schemeUrlNodes.forEach(node => {
            const linkElement = node.querySelector('a');
            if (linkElement) {
              schemeUrlList.push(linkElement.href);
            }
          });
          return schemeUrlList;
        });
  
        allSchemeUrlList.push(...moreSchemeUrls);
      }
    }
    await browser.close()
    return allSchemeUrlList.slice(1)
  }

async function schemeDetails(){
  const schemeUrlList = await schemeUrls()
  browser = await puppeteer.launch()
  page = await browser.newPage()
  const allSchemes = []
  for (const schemeUrl of schemeUrlList){
        console.log("ispe Gaya:", schemeUrl)
    await page.goto(schemeUrl)
    const result = await page.evaluate(()=>{

    const extractText = (selector) => {
        const element = document.querySelector(selector);
        return element ? element.innerText.trim() : null;
    };

    const extractListItems = (selector) => {
        return Array.from(document.querySelectorAll(`${selector} li`)).map(li => li.innerText.trim());
    };

    const extractSteps = (selector) => {
        return Array.from(document.querySelectorAll(selector)).map(step => step.innerText.trim());
    };

    const scheme = {
        title: extractText('.inner-head-left h2'),
        department: extractText('.top-bage-wrapper .badge:first-child'),
        type: Array.from(document.querySelectorAll('.mid-bage-wrapper .badge')).map(badge => badge.innerText.trim()),
        overview: extractText('#Overview p'),
        benefits: extractListItems('#Benefits ul'),
        eligibility: extractListItems('#Eligibility ul'),
        applicationProcess: extractSteps('.application p'),
        requirements: extractListItems('#Requirements ul'),
    };
    return scheme;
    })
    allSchemes.push({...result, scheme_link: schemeUrl ,id: uuidv4()})

} await browser.close()
    console.log("These are the schemes:",allSchemes)
  return allSchemes
  
  
}

schemeDetails()

async function main(){
  const allSchemeData = await schemeDetails()
  const targetDir = path.join(__dirname, '..','..','scrapedData');
  const filePath = path.join(targetDir, 'uttarPradesh.json');
  fs.writeFileSync(filePath, JSON.stringify(allSchemeData, null, 2), 'utf-8');
}

