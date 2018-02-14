#!/bin/sh

rm -rf db

bin/rengu load verse verses/*
bin/rengu load source sources/*
bin/rengu load author authors/*

