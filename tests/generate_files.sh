# Script to generate random files 
TARGET="example-test"
NUM_FILES=$1

# Subdirectory creation params
NUM_SUBDIRECTORIES=5
MIN_SUB_FILES=5
MAX_SUB_FILES=15

if [ $NUM_SUBDIRECTORIES -gt $NUM_FILES ]; then
    NUM_SUBDIRECTORIES=$NUM_FILES
fi 

mkdir -p "$TARGET"

echo "Creating $1 random files in /$TARGET..."

# Array of extensions to use wen creating files 
EXTENSIONS=("jpg" "png" "pdf" "docx" "txt" "mp3" "zip" "py" "unknown" "mp4" "xlsl" "sh" "odt" "pages" "json" "sql" "tar" "db" "sh")

get_random_extension(){
    local ext=${EXTENSIONS[$RANDOM % ${#EXTENSIONS[@]}]}
    echo "$ext"
}

# Create NUM_FILES (user passed argument) random files
for ((i=1; i<=NUM_FILES; i++))
do  
    # Pick a random extension from the list
    EXT=$(get_random_extension)

    # Create sub-directories with random files in them
    if [ "$i" -le "$NUM_SUBDIRECTORIES" ]; then 

        num_subfiles=$(shuf -i $MIN_SUB_FILES-$MAX_SUB_FILES -n 1)
        SUB_DIR_NAME="sub_dir_$i"

        mkdir -p "$TARGET/$SUB_DIR_NAME"
        for ((j=1; j<=num_subfiles; j++))
        do 
            SUB_EXT=$(get_random_extension)
            touch "$TARGET/$SUB_DIR_NAME/sub_test_file_$i.$j.$SUB_EXT"
        done 
    fi
    
    # Create the file
    touch "$TARGET/test_file_$i.$EXT"
done