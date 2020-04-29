export MODE=$1

if [ $# -eq 0 ]
then
    echo "########################################################################"
    echo "##    No Arguments were passed.                                         "
    echo "##"
    echo "##    Run Python Module to fetch Notifications from University website."
    echo "##"
    echo "##    Syntax : run.sh 1|2|3"
    echo "##    Options:"
    echo "##    1    Print Updates to console only."
    echo "##    2    Print all notifications to console only."
    echo "##    3    Write data to a text file."
    echo "##    4    Download all notifications pdf files."
    echo "##"
    echo "##    Text files and PDFs will be saved in ./Data Folder."
    echo "##"
    echo "########################################################################"

else
    if (($MODE == "1"))
    then
        python -m src.UniversityFetch 1
    elif (($MODE == "2"))
    then
        python -m src.UniversityFetch 2
    elif (($MODE == "3"))
    then
        python -m src.UniversityFetch 3
    elif (($MODE == "4"))
    then
        python -m src.UniversityFetch 4
    else
        echo "Wrong option!"
    fi
fi
