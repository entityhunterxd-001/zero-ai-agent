use reqwest::blocking::get;
use scraper::{Html, Selector};
use serde::Serialize;
use std::env;

#[derive(Serialize)]
struct ScrapedData {
    url: String,
    title: String,
    description: String,
    content: String,
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <URL>", args[0]);
        std::process::exit(1);
    }

    let url = &args[1];

    let response = match get(url) {
        Ok(res) => res,
        Err(e) => {
            eprintln!("Failed to fetch URL: {}", e);
            std::process::exit(1);
        }
    };

    let body = match response.text() {
        Ok(text) => text,
        Err(e) => {
            eprintln!("Failed to read response body: {}", e);
            std::process::exit(1);
        }
    };

    let document = Html::parse_document(&body);
    
    let title_selector = Selector::parse("title").unwrap();
    let desc_selector = Selector::parse("meta[name='description']").unwrap();
    let heading_selector = Selector::parse("h1, h2, h3").unwrap();
    let paragraph_selector = Selector::parse("p").unwrap();

    let title = document.select(&title_selector).next().map(|el| el.text().collect::<Vec<_>>().join(" ")).unwrap_or_else(|| "No Title".to_string());
    let description = document.select(&desc_selector).next().and_then(|el| el.value().attr("content")).unwrap_or("No Description").to_string();

    let mut content_parts = Vec::new();
    
    for heading in document.select(&heading_selector) {
        let text = heading.text().collect::<Vec<_>>().join(" ").trim().to_string();
        if !text.is_empty() { content_parts.push(format!("\n## {}", text)); }
    }

    for paragraph in document.select(&paragraph_selector) {
        let text = paragraph.text().collect::<Vec<_>>().join(" ").trim().to_string();
        if !text.is_empty() { content_parts.push(text); }
    }

    let content = content_parts.join("\n\n");

    let output = ScrapedData { url: url.clone(), title, description, content };
    println!("{}", serde_json::to_string(&output).unwrap());
}