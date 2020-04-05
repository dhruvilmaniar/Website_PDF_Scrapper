export MODE=$1


if (($MODE == "1"))
then
    echo "Showing output to the console only..."
    python -m src.UniversityFetch 1
elif (($MODE == "2"))
then
    echo "Showing output in Text File..."
    python -m src.UniversityFetch 2
elif (($MODE == "3"))
then
    echo "Getting the PDF Files..."
    python -m src.UniversityFetch 3
else
    echo "More coming soon..."
fi
