set -x

pushd rl_bot

rm -rf vrep
mkdir vrep

pushd vrep

echo "Finding vrep"
vrep_file=`find / | grep /programming/remoteApiBindings/python/python/vrep.py`
vrep_consts_file=`dirname $vrep_file`/vrepConst.py
remote_api_so_file=`dirname $vrep_file`/../../lib/lib/Linux/64Bit/remoteApi.so
remote_api_dylib_file=`dirname $vrep_file`/../../lib/lib/Mac/remoteApi.dylib

if [ -z $vrep_file ]
then
    echo "Could not find vrep.py. Please check if vrep correctly installed."
    exit 1
fi

cp $vrep_file .
cp $vrep_consts_file .
cp $remote_api_so_file .
cp $remote_api_dylib_file .

# Make python3 compatible
sed 's/from vrepConst/from .vrepConst/g' vrep.py > _vrep.py
mv _vrep.py vrep.py

popd
popd