from StringIO import StringIO
import logging


def main():


    def downsample_to_proportion(rows, proportion):
        
        counter = 0.0
        last_counter = None
        results = []

        for row in rows:

            counter += proportion

            if int(counter) != last_counter:
                results.append(row)
                last_counter = int(counter)

        return results

    array = []

    for i in range(1,11):

        array.append(i)

    print array
    answer = downsample_to_proportion(array, 0.5)
    print answer



main()
