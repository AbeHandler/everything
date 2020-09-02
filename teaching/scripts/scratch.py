
##How to delete folders

course = canvas.get_course(COURSES[args.course])

for f in course.get_folders():
    if str(f) != "root":

        try:
            # https://github.com/ucfopen/canvasapi/blob/develop/canvasapi/folder.py#L122
            f.delete(force=True)

        except:
            pass