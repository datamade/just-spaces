# Define the variables that we'll use to create the GPG key and export it to
# the server. All the work that is done on your local machine is done inside
# a temporary folder.
TMPDIR:=$(shell mktemp -d)

# The "name" that will be associated with the key. Make it a human friendly
# name for your project
NAME=Just Spaces Production Key

# GPG uses an email address as a easier to remember way to lookup keys on your
# keyring. While they are not required to be unique, for the purposes of this
# setup, please ensure that it is unique.
EMAIL=justspaces+production@datamade.us

# The hostname for your project. You will need to make sure that the DNS is
# configured to point this domain at the correct server IP address before
# running this makefile
SERVER=justspacesproject.org

# The name of your project. This should match the name of the github
# repository.
PROJECT=just-spaces

# One way to configure the way that the gpg command line tool generates keys is
# to pass the configuration options to it on the command line as opposed to the
# regular interactive way. This defines a variable that can be used in that
# way.
define GPG_SETUP
%echo Generating a basic OpenPGP key\n
%no-protection\n
Key-Type: RSA\n
Key-Length: 4096\n
Key-Usage: sign\n
Subkey-Type: RSA\n
Subkey-Length: 4096\n
Subkey-Usage: encrypt\n
Name-Real: $(NAME)\n
Name-Email: $(EMAIL)\n
Expire-Date: 0\n
%commit\n
%echo done\n
endef

# Export the variable defined above as an environmental variable so it can be
# used in the targets below.
export GPG_SETUP

.PHONY: all key
# The default 'all' target will generate a key and upload it to the remote
# server that you configured using the variables above.
all : transfer indoctrinate

# Use this target for testing purposes if you only want to generate the key and not
# upload it to a server.
key : $(TMPDIR)/pubring.gpg

# Turn the environmental variable used to configure the --gen-key command into
# a target which will, in effect, get "echoed" into the command when the time
# comes.
.INTERMEDIATE: gpg_setup
gpg_setup :
	echo $$GPG_SETUP > $@

# Generate the key using the configuration options defined above and force the
# command line tool to not prompt for any interactive commands by giving it the
# "--batch" flag.
$(TMPDIR)/pubring.gpg : gpg_setup
	gpg --homedir=$(TMPDIR) --batch --gen-key $<

# Export the private portion of the key.
$(TMPDIR)/private.key : $(TMPDIR)/pubring.gpg
	gpg --homedir=$(TMPDIR) --export-secret-keys $(EMAIL) > $@

# Export the public portion of the key
$(TMPDIR)/public.key : $(TMPDIR)/pubring.gpg
	gpg --homedir=$(TMPDIR) --export -a $(EMAIL) > $@

# Make a directory on the target server within the .gnupg folder of the
# datamade user to hold the key. Transfer the key to the server and then import
# it into the keyring for the datamade user.
transfer: $(TMPDIR)/private.key
	-ssh ubuntu@$(SERVER) 'sudo -u datamade mkdir -p /home/datamade/.gnupg/$(PROJECT)'
	rsync -a --rsync-path="sudo -u datamade rsync" $< ubuntu@$(SERVER):/home/datamade/.gnupg/$(PROJECT)
	ssh ubuntu@$(SERVER) 'sudo -u datamade -H gpg --import /home/datamade/.gnupg/$(PROJECT)/private.key'

# Add the key to the blackbox setup for the project and then re-encrypt all the
# encrypted files.
indoctrinate : $(TMPDIR)/public.key
	blackbox_addadmin $(EMAIL) $(TMPDIR)
	blackbox_update_all_files
