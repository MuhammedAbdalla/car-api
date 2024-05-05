# Create a temporary directory to store the build context
mkdir -p tmp-context

# Copy the file that you need to the temporary directory
cp ../requirements.txt tmp-context
cp ../Authentication.py tmp-context
cp ../Modules.py tmp-context
cp ../Monitor.py tmp-context
cp ../QueueSystem.py tmp-context
cp ../tests/tests.py tmp-context

# Build the image from the temporary directory
docker-compose build

# Remove the temporary directory
rm -rf tmp-context