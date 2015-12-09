#!/bin/sh
if [ $# -ne 2 ] ; then
        echo "Usage: Conf_Name Control_Name"
        exit 1
fi
CNF_NAME=$1
CTRL_NAME=$2
echo "begin remote" >> ~/$CNF_NAME
echo >> ~/$CNF_NAME
echo "  name  "$CTRL_NAME >> ~/$CNF_NAME
echo "  flags RAW_CODES"    >> ~/$CNF_NAME
echo "  eps       30" >> ~/$CNF_NAME
echo "  aeps     100" >> ~/$CNF_NAME
echo "  gap   100000" >> ~/$CNF_NAME
echo >> ~/$CNF_NAME
echo "      begin raw_codes" >> ~/$CNF_NAME
echo >> ~/$CNF_NAME
ls ~/lirc/ | while read FILES
do
echo "Generate "$FILES" Botton..."
sleep 2
echo "          name "$FILES >> ~/$CNF_NAME
cat ~/lirc/$FILES | sed '1d' | sed 's/^.....//' | sed 'N;N;N;N;N;s/\n/\t/g;' >> ~/$CNF_NAME
echo >> ~/$CNF_NAME
done
echo "      end raw_codes" >> ~/$CNF_NAME
echo >> ~/$CNF_NAME
echo "end remote" >> ~/$CNF_NAME
echo >> ~/$CNF_NAME
