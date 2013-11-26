file-tools
==========

Miscellaneous tools for keeping file systems clean and tidy. Some of these could do with a bit of tidying up some time. I use them regularly on servers and for managing files at home. To use them, you will probably need to do a bit of editing as they don't have lots of command line options.

 * **check_dir_contains_files** - Goes though all files in one directory and checks they exist in another. Checks files match in size and checksum.
 * **photo_organiser** - Moves image files from one directory to a destination based on a directory structure in the form of year/month/day. Dates are read from EXIF data.
 * **check_valid_images** - Reads all images in a directory and shows if any could not be decoded.
 * **disk_full** - Run this regularly from a cron job and you'll be emailed when any of the disks fill up past a certain percentage.
 * **du_log** - Stores disk usage of the file system by directory over time. It's designed to be run once a day (but can be run less frequently or irregularly) and makes a compressed file for each day.
 * **du_compare** - Used to compare two log files generated by du_log. It shows which directories grew or shrunk the most over the period, ordered with the biggest increasing directory at the top.
