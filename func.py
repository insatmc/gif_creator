import os
import imageio

def handler(event,context):
  files = event["files"]
  name = event["name"]
  bucket = event["bucket"]
  i = 0
  filenames = []
  for file in files:
    filename = "im-"+str(name)+"-"+str(i)+".png"
    fh = open(filename, "wb")
    filenames.append(filename)
    i = i + 1
    fh.write(file.decode('base64'))
    fh.close
  images = []
  for filename in filenames:
    images.append(imageio.imread(filename))

  imageio.mimsave(name+'.gif', images)
  fh = open(name+'.gif', "rb")
  s3.Object(bucket, name+'.gif').put(
    Body=fh,
    ACL='public-read',
    Metadata={
      'Content-Type': 'image/gif'
    }
  )
  for filename in filenames:
      os.remove(filename)
  return {"bucket": bucket, "filename": name+".gif"
