#!/usr/bin/env python

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

def md_rename_file(input_map, output_path, new_filename, mod_name):
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

    def update_map_names(offset):
        """Given the offset of '...\\mp_map_list', updates the map names."""
        map_names_offset = read_uint32(offset + 0x14) - map_magic + 0x1B0

        def replace_wide_name(offset, old_name, new_name):
            """Replaces a utf16 name with another utf16 string"""
            clear_and_write_bytes(offset, (len(old_name) + 1) * 2, new_name.encode('utf-16le'))

        replace_wide_name(map_names_offset + 0x48,  "Rat Race",         "Random")
        replace_wide_name(map_names_offset + 0xB4,  "Boarding Action",  "Barrier")
        replace_wide_name(map_names_offset + 0xD4,  "Blood Gulch",      "Blood Gulch")
        replace_wide_name(map_names_offset + 0x174, "Infinity",         "Crossing")
        replace_wide_name(map_names_offset + 0x1A0, "Gephyrophobia",    mod_name)

    def update_map_descriptions(offset):
        """Given the offset of '...\\map_data', updates the map descriptions."""
        map_descr_offset = read_uint32(offset + 0x14) - map_magic + 0x19C

        originalBloodgulchBytes = bytes([
            0x54, 0x00, 0x68, 0x00, 0x65, 0x00, 0x20, 0x00, 0x51, 0x00, 0x75, 0x00, 0x69, 0x00, 0x63, 0x00,
            0x6B, 0x00, 0x20, 0x00, 0x0D, 0x00, 0x0A, 0x00, 0x61, 0x00, 0x6E, 0x00, 0x64, 0x00, 0x20, 0x00,
            0x74, 0x00, 0x68, 0x00, 0x65, 0x00, 0x20, 0x00, 0x44, 0x00, 0x65, 0x00, 0x61, 0x00, 0x64, 0x00,
            0x0D, 0x00, 0x0A, 0x00, 0x0D, 0x00, 0x0A, 0x00, 0x34, 0x00, 0x2D, 0x00, 0x31, 0x00, 0x36, 0x00,
            0x20, 0x00, 0x70, 0x00, 0x6C, 0x00, 0x61, 0x00, 0x79, 0x00, 0x65, 0x00, 0x72, 0x00, 0x73, 0x00,
            0x0D, 0x00, 0x0A, 0x00, 0x0D, 0x00, 0x0A, 0x00, 0x53, 0x00, 0x75, 0x00, 0x70, 0x00, 0x70, 0x00,
            0x6F, 0x00, 0x72, 0x00, 0x74, 0x00, 0x73, 0x00, 0x20, 0x00, 0x76, 0x00, 0x65, 0x00, 0x68, 0x00,
            0x69, 0x00, 0x63, 0x00, 0x6C, 0x00, 0x65, 0x00, 0x73, 0x00])

        clear_and_write_bytes(map_descr_offset + 0x12C, 0x56,   "Where would you\r\nlike to go?".encode("utf-16le"))
        clear_and_write_bytes(map_descr_offset + 0x2BC, 0x48,   "So Close,\r\nYet So Far..".encode("utf-16le"))
        write_bytes(          map_descr_offset + 0x308,         originalBloodgulchBytes)
        clear_and_write_bytes(map_descr_offset + 0x634, 0x86,   "A Memorial to\r\nHeroes Fallen".encode("utf-16le"))
        clear_and_write_bytes(map_descr_offset + 0x740, 0x64,   "Modded".encode("utf-16le"))


    # process the map header
    game_version = read_uint32(0x4)
    index_header_offset = read_uint32(0x10)

    if game_version != 7:
        print('This is not a valid (version 7) full-version map!')

    # process the index header
    index_offset = read_uint32(index_header_offset)
    tag_count = read_uint32(index_header_offset + 0xC)
    index_entry_offsets = (index_offset + 0x20 * i for i in range(tag_count))

    map_magic = index_offset - index_header_offset

    # write the new internal name
    clear_and_write_bytes(0x20, 0xF, new_filename.encode('ascii'))

    for curr_offset in index_entry_offsets:
        # skipping tags of class ustr
        if read_bytes(curr_offset, 0x4) != b'rtsu':
            continue

        name_offset = read_uint32(curr_offset + 0x10) - map_magic

        if has_bytes(name_offset, b'ui\\shell\\main_menu\\mp_map_list'):
            update_map_names(curr_offset)

        elif has_bytes(name_offset, b'ui\\shell\\main_menu\\multiplayer_type_select\\mp_map_select\\map_data'):
            update_map_descriptions(curr_offset)

    # save under a new filename
    with open(output_path, "wb") as outputFile:
        outputFile.write(map_buffer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Converts a map to MD format by updating the internal map names.')
    parser.add_argument('input_map', help='Path to the Halo mapfile to rename.')
    parser.add_argument('mod_name', help='User friendly name of the mod. Must be <= 13 characters. This is the name that shows in the map selection menu in-game.')
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

        elif len(args.mod_name) > 13:
            print("Mod name must be less than 13 characters")

        elif len(new_filename) > 13:
            print("Map name '%s' is too long. Try shortening the short name" % new_filename)

        elif args.short_name.lower() != args.short_name:
            print("Map name '%s' has capital letter. The short name must be all lowercase" % args.short_name)

        elif os.path.exists(output_path):
            print("Map already exists at %s ..aborting for safety.." % output_path)

        else:
            md_rename_file(args.input_map, output_path, new_filename, args.mod_name)

    finally:
        # for au3 GUI post mortem
        print()
        os.system("pause")
