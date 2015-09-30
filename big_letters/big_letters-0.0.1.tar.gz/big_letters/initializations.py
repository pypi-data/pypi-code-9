letters = """
 ***
*   *
*****
*   *
*   *

****
*   *
****
*   *
****

 ****
*
*
*
 ****

****
*   *
*   *
*   *
****

*****
*
***
*
*****

*****
*
***
*
*

 ****
*
*  **
*   *
 ****

*   *
*   *
*****
*   *
*   *

***
 *
 *
 *
***

 ****
    *
    *
*   *
 ***

*  *
* *
**
* *
*  *

*
*
*
*
*****

*   *
** **
* * *
*   *
*   *

*   *
**  *
* * *
*  **
*   *

 ***
*   *
*   *
*   *
 ***

****
*   *
****
*
*

 ***
*   *
* * *
*  **
 *** *

****
*   *
****
*  *
*   *

 ****
*
 ****
     *
 ****

*****
  *
  *
  *
  *

*   *
*   *
*   *
*   *
 ***

*     *
*     *
 *   *
  * *
   *

*     *
*     *
*  *  *
*  *  *
 ** **

*   *
 * *
  *
 * *
*   *

*   *
 * *
  *
  *
  *

*****
   *
  *
 *
*****
"""

letters = letters.strip("\n")
lines = letters.split("\n")

letters= {}

space = ["     "] * 5

for i in range(26):
    letter_lines = lines[i * 6 : i * 6 + 5]
    char = chr(65 + i)
    letters[char] = letter_lines

for char, lines in letters.items():
    n = max(len(l) for l in lines)
    newl = []
    for l in lines:
        newl.append(l + (n - len(l)) * " ")
    letters[char] = newl
