
filename="combined.csv"
fileid="15AUtAHF6LwpWd5XHk3wwAd6lIYznRJNl"


fileid="### file id ###"
filename="MyFile.csv"
html=`curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}"`
curl -Lb ./cookie "https://drive.google.com/uc?export=download&`echo ${html}|grep -Po '(confirm=[a-zA-Z0-9\-_]+)'`&id=${fileid}" -o ${filename}