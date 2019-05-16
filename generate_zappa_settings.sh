#!/usr/local/bin/bash

TERRAFORM_DIR="terraform"

cd $TERRAFORM_DIR
declare -A $(terraform output | awk -F' = ' '{print "VARS[" $1 "]=" $2}')

cd -
cp zappa_settings.json.template zappa_settings.json.intermediate
for var_name in "${!VARS[@]}"
do
  var_value=${VARS[$var_name]}
  echo "var_name: $var_name, value: $var_value"
  sed -i '' "s#\$$var_name#$var_value#g" zappa_settings.json.intermediate
done

cp zappa_settings.json zappa_settings.json.bak
cp zappa_settings.json.intermediate zappa_settings.json
rm zappa_settings.json.intermediate