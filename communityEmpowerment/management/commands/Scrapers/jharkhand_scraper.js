const puppeteer = require('puppeteer')
const {v4: uuidv4} = require('uuid')
const fs = require('fs').promises


const getAllUrls = async function(){
    const url = "https://jharkhand.gov.in/Home/SearchSchemes"
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    await  page.goto(url , {timeout:60000})

    const values = await page.evaluate(() => {
        const options = Array.from(document.querySelector('select').children); 
        return options.map(option => {
            return {
                value: option.value,
                departmentName: option.innerText.trim() 
            };
        });
    });

    await browser.close()
    return values 
}

async function get_pdf_link(url, departmentName) {
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    await  page.goto(url , {timeout:60000})
    const result = await page.evaluate(()=>{
        const rows = document.querySelectorAll('tbody tr')
        const data = []
        rows.forEach((row, index)=>{
            if(index === 0) return;
            const title = row.children[1].innerText.trim()
            const publishDate = row.children[5].innerText.trim()
            const pdfUrl = row.children[6].children[0].href
            data.push({title,publishDate, pdfUrl})
        })
        return data 
    })

    const resultWithUUID = result.map((item)=>({id:uuidv4(), ...item, departmentName}))

    await browser.close()
    return resultWithUUID

}

async function scrapeJharkhandScholarships(){
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    await page.goto("https://ekalyan.cgg.gov.in/")
    const result = await page.evaluate(()=>{
        const descriptionList = []
        const allSchemes = []
        const preAndPostMatricSchemeNodes = document.querySelectorAll(".schemes .container .row .col-md-4 ul li:not(:nth-child(1))")
        // const postMatricSchemeNodes = document.querySelectorAll(".container .row :nth-child(4) ul li:not(:nth-child(1))")
        const descriptionNodes = document.querySelectorAll("#pills-tabContent #pills-home .block-hdnews ul li:not(:last-child)")
        descriptionNodes.forEach((node)=>{
            const description = node.textContent
            descriptionList.push(description)
        })

        preAndPostMatricSchemeNodes.forEach((node)=>{
            const title = node.textContent.trim()
            const scheme = {
                title,
                description: [...descriptionList],
                id: self.crypto.randomUUID(),
                schemeUrl: "https://ekalyan.cgg.gov.in/"
            }
            allSchemes.push(scheme)
        })

        return allSchemes

        
    })
    await browser.close()
    return result
}




async function main() {
    const allResults = []
    const values = await getAllUrls()
    await Promise.all(values.map(async (item) => {
        const res = await get_pdf_link(`https://jharkhand.gov.in/Home/SearchSchemes?department=${item.value}`, item.departmentName)
        allResults.push(...res)
    }))

    const jharkhandScholarships = await scrapeJharkhandScholarships()
    const targetDir = path.join(__dirname, '..','..','scrapedData', 'scrapedPdfs');
    const filePath = path.join(targetDir, 'jharkhandPdf.json');

    const targetDir2 = path.join(__dirname, '..','..','scrapedData');
    const filePath2 = path.join(targetDir, 'jharkhand.json');

    await fs.writeFile(filePath, JSON.stringify(allResults, null, 2))
    await fs.writeFile(filePath2, JSON.stringify(jharkhandScholarships, null, 2))
}
main()




