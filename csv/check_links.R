#!/usr/bin/env Rscript

# Check validity of URLs in CSV files.

# Check for required package
if (!requireNamespace("httr", quietly = TRUE)) {
  stop("Package 'httr' is needed for this script to work. Please install it with install.packages('httr').", call. = FALSE)
}

check_url <- function(url) {
  # User agent similar to the Python script
  ua <- httr::user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
  
  tryCatch({
    # Try HEAD first to save bandwidth
    response <- httr::HEAD(url, ua, httr::timeout(10))
    status <- httr::status_code(response)
    
    if (status >= 400) {
      # Fallback to GET if HEAD fails (some servers block HEAD)
      response <- httr::GET(url, ua, httr::add_headers(Range = "bytes=0-10"), httr::timeout(10))
      status <- httr::status_code(response)
    }
    
    if (status < 400) {
      return(list(success = TRUE, status = status))
    } else {
      return(list(success = FALSE, status = status))
    }
  }, error = function(e) {
    return(list(success = FALSE, status = e$message))
  })
}

check_links <- function(csv_paths) {
  has_errors <- FALSE
  # Initialize data frame to store link details
  link_report <- data.frame(
    file = character(),
    row_number = integer(),
    title_item = character(),
    link = character(),
    status = character(),
    success = logical(),
    stringsAsFactors = FALSE
  )
  
  for (path in csv_paths) {
    if (!file.exists(path)) {
      message(sprintf("File not found: %s", path))
      next
    }
    
    message(sprintf("Checking file: %s", path))
    
    # Read CSV
    # Using base R read.csv to avoid extra dependencies like readr/tidyverse if possible,
    # but ensuring strings are not factors.
    tryCatch({
      df <- read.csv(path, stringsAsFactors = FALSE, encoding = "UTF-8")
    }, error = function(e) {
      message(sprintf("Failed to read %s: %s", path, e$message))
      return(NULL) 
    })
    
    if (is.null(df)) next
    
    if (!"asset_links" %in% names(df)) {
      message(sprintf("'asset_links' column missing in %s", path))
      next
    }
    
    # Iterate through rows
    for (i in seq_len(nrow(df))) {
      asset_links <- df$asset_links[i]
      
      # Skip if empty or NA
      if (is.na(asset_links) || trimws(asset_links) == "") {
        next
      }
      
      # Handle space separator
      links <- strsplit(asset_links, " ")[[1]]
      
      for (link in links) {
        link <- trimws(link)
        if (link == "") next
        
        result <- check_url(link)
        item_title <- if ("title_item" %in% names(df)) df$title_item[i] else sprintf("Row %d", i + 1)
        
        if (!result$success) {
          has_errors <- TRUE
          message(sprintf("Broken link in '%s': %s (Status: %s)", item_title, link, result$status))
        }
        
        # Add to report
        link_report <- rbind(link_report, data.frame(
          file = path,
          row_number = i + 1, # Assuming header row exists
          title_item = item_title,
          link = link,
          status = as.character(result$status),
          success = result$success,
          stringsAsFactors = FALSE
        ))
      }
    }
  }
  
  write.csv(link_report, "link_report.csv", row.names = FALSE)
  message("Full link report saved to 'link_report.csv'.")

  if (has_errors) {
    quit(status = 1)
  } else {
    message("All links checked successfully.")
  }
}

# Main execution
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  # Default paths based on project structure
  paths <- c("csv/hazard.csv", "csv/expvul.csv")
} else {
  paths <- args
}

check_links(paths)
