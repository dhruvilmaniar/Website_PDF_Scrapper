export MODE=$1


if (($MODE == "1"))
then
    python -m src.UniversityFetch 1
elif (($MODE == "2"))
then
    python -m src.UniversityFetch 2
elif (($MODE == "3"))
then
    python -m src.UniversityFetch 3
else
    echo "Argument not supported yet.."
fi
