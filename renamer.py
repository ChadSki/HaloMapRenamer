#!/usr/bin/env python

# Copyright (c) 2014, Chad Zawistowski
# All rights reserved.
# 
# Copyright (c) 2014, Null <foo.null@yahoo.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import struct
import argparse

def rename_mapfile(input_map, output_path, new_filename):
    with open(input_map, 'rb') as input_file:
        map_buffer = bytearray(input_file.read())

    def has_bytes(offset, bytes):
        """Returns true if the bytes at the offset match our bytestring."""
        return map_buffer[offset:offset + len(bytes)] == bytes

    def read_bytes(offset, length):
        """Reads <length> bytes from the specified offset."""
        return map_buffer[offset:offset + length]

    def write_bytes(offset, data):
        """Writes bytes to the specified offset."""
        map_buffer[offset:offset + len(data)] = data

    def clear_and_write_bytes(offset, num_zeroes, data):
        """Writes a number of null bytes, then writes data to the specified offset."""
        write_bytes(offset, b'\x00' * num_zeroes)
        write_bytes(offset, data)

    def read_uint32(offset):
        """Reads a little-endian int32 from the specified offset."""
        return struct.unpack('<I', read_bytes(offset, 0x4))[0]

    if not has_bytes(0x0, b'daeh'):
        print('This is not a valid map! (First four bytes should spell "daeh")')
        return

    # write the new internal name
    clear_and_write_bytes(0x20, 0xF, new_filename.encode('ascii'))

    # save under a new filename
    with open(output_path, "wb") as outputFile:
        outputFile.write(map_buffer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts a map to MD format by updating the internal map names.')
    parser.add_argument('input_map', help='Path to the Halo mapfile to rename.')
    parser.add_argument('short_name', help='Internal name of the mod, and the new filename. Must be all lowercase and >= 1 character(s).')
    parser.add_argument('build_number', type=int, help='The build number of the mod which is also used in the outputting filename. This should be increased before any sort of public or private distribution. Must be an integer >= 1.')
    parser.add_argument('output_directory', nargs='?', help='Directory to output the new MD renamed map in. This is optional and defaults to the directory <input_map> is in.')

    try:
        args = parser.parse_args()

        if args.output_directory == None:
            args.output_directory = os.path.dirname(args.input_map)

        new_filename = "%s_%d" % (args.short_name, args.build_number)
        output_path = os.path.join(args.output_directory, new_filename + ".map")

        if not os.path.exists(args.input_map) or not args.input_map.endswith(".map"):
            print("%s is not a .map file" % args.input_map)

        elif os.path.isdir(args.input_map):
            print("%s is a directory.. which is not good" % args.input_map)

        elif args.build_number <= 0:
            print("Build number is too small")

        elif len(new_filename) > 13:
            print("Map name '%s' is too long. Try shortening the short name" % new_filename)

        elif args.short_name.lower() != args.short_name:
            print("Map name '%s' has capital letter. The short name must be all lowercase" % args.short_name)

        elif os.path.exists(output_path):
            print("Map already exists at %s ..aborting for safety.." % output_path)

        else:
            rename_mapfile(args.input_map, output_path, new_filename)
            print("Successfully renamed to %s" % new_filename + ".map")

    finally:
        # for au3 GUI post mortem
        print()
        os.system("pause")
