### Project Details:
Simplest Python web scrapper, to :
- Fetch all the notifications appearing on my University website
- Saving them as text file (parameters saved : Date, Title, PDF link) 
- Downloading Circulars posted by the University in Local Machine.

### Usage:
Use bash to clone or download this repository.

For bash use:
```git clone https://github.com/dhruvilmaniar/Website_PDF_Scrapper```

After that, run the following command:
```pip install -r requirenments.txt```

After that, run ```sh run.sh``` or ```run.sh``` based on your system.
You should now see various options allowed as args.


#### Need for this:
It was a tedious task for me to go to the website and check for any updates during quarantine period.

#### More
- Playing with my University website from dev tools, I observed that each notifications share some common attributes. Using these to fetch only notifications from the site.
- The pdfs are stored in the Data/ folder.
- Being good at shell scripting is still a dream for me.

### Todos:
- [x] Run via shell script
- [x] Add logging instead of printing


