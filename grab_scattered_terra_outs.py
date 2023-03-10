import os
import argparse

arg = argparse.ArgumentParser(prog = 'grab scattered terra outs', 
	description = "Download scattered workflow outputs when Terra's UI "
	"isn't cooperating by directly evoking gsutil (REQUIRES gsutil to be set up and authenticated).")
arg.add_argument('--bucket', default="fc-caa84e5a-8ef7-434e-af9c-feaf6366a042", required=False)
arg.add_argument('--submission_id', required=True)
arg.add_argument('--workflow_name', default="myco", required=False)
arg.add_argument('--workflow_id', required=True)
arg.add_argument('--task', default="make_mask_and_diff", required=False)
arg.add_argument('--cacheCopy', type=bool, default=False, required=False)
arg.add_argument('--glob', type=bool, default=False, required=False)
arg.add_argument('--file', default="*.diff", required=False)
args = arg.parse_args()

path = f"gs://{args.bucket}/submissions/{args.submission_id}/{args.workflow_name}/{args.workflow_id}/call-{args.task}/"
base = []
if args.cacheCopy == True:
	base.append("cacheCopy/")
if args.glob == True:
	base.append("glob*/")
base.append(f"{args.file}")
print(f'Constructed path:\n{path}shard-(whatever)/{"".join(base)}')

shards = list(os.popen(f"gsutil ls {path}"))

uris = []
for shard in shards:
	uri = shard[:-1] + "".join(base)
	uris.append(f'\"{uri}\"')

if len(uris) > 998:
	print("Splitting into smaller downloads...")
	list_of_smallish_lists_of_uris = [uris[i:i + 998] for i in range(0, len(uris), 998)]
	for smallish_list_of_uris in list_of_lists_of_uris:
		uris_as_string = " ".join(smallish_list_of_uris)
		command = f"gsutil -m cp {uris_as_string} ."
		print(f"Running {command}\n\n")
		os.system(command)
else:
	uris_as_string = " ".join(uris)
	command = f"gsutil -m cp {uris_as_string} ."
	# doesn't seem to consistently work as a subshell, so just let the user copy-paste
	print(f"Running the following command:\n\n{command}\n\n")
