# These are example settings for organising photos with photo_organiser.
# Test with sample images first to make sure you are set-up correctly and
# confident with the tool. Photos will be moved from their original position.
# No responsibility taken for loss of your precious photos.


INPUT_PATHS = [
    '/media/username/*/DCIM',
]
OUTPUT_FILTERS = [
    {
        'EXTENSIONS': ['jpg', 'jpeg', 'mov', 'mp4', 'm4v', '3gp'],
        'PATH': '/path/to/nas/photos',
    },
    {
        'EXTENSIONS': ['cr2',],
        'PATH': '/path/to/nas/raw-photos',
    },
]

