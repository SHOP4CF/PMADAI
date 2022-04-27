# A script that checks if a development environment exists and if not then it creates
# If it exists, it updates the env

# It's good to execute the script before testing the project (executing `make test`)

modules="processing preprocessing backend data_collection kafka-orion-alert orion-kafka-bridge prediction"
echo "Creating or updating virtual environments"
for module in $modules; do
    cd $module
    if [ -d "venv" ]
    then
        echo "venv exists in $module -> updating..."
    else
        echo "venv does not exist in $module -> creating..."
        python -m venv venv # crates virtual environment within module, named `venv`
    fi
    # Activate the venv (depending on OS)
    if [[ $OSTYPE == 'linux' ]]
    then
        source venv/bin/activate
    elif [[ $OSTYPE == 'msys' ]]
    then
        source venv/Scripts/activate
    fi
    pip install -r requirements.txt
    deactivate
    cd ..
done
