import os

def createIfNotExists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
def move(folderName,files):
    for file in files:
        os.replace(file,f"{folderName}/{file}")
            
files= os.listdir()
print(files)
files.remove("main.py")
print(files)
createIfNotExists("Docs")
createIfNotExists("Images")
createIfNotExists("Media")
createIfNotExists("Others")
imgExts= [".png",".jpg",".jpeg"]
docExts= [".txt",".docx",".doc",".pdf"]
mediaExts=[".mp4",".mp3",".flv"]
images= [file for file in files if os.path.splitext(file)[1].lower() in imgExts]
docs= [file for file in files if os.path.splitext(file)[1].lower() in docExts]
print(docs)
medias= [file for file in files if os.path.splitext(file)[1].lower() in mediaExts]

#remaining files in othr folder
others=[]
for file in files:
    ext= os.path.splitext(file)[1].lower()
    if (ext not in mediaExts) and (ext not in docExts) and (ext not in imgExts) and os.path.isfile(file):
        others.append(file)
print(others)
move("Docs",docs)
move("Images",images)

move("Media",medias)
move("Others",others)         
         
