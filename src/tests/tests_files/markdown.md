# Headings

# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

### Edge Cases for Headings
#HeadingWithoutSpace  
# Heading with trailing hashes ###  
   ## Heading with leading spaces  
###### Excessive hashes #######  
#  

# Emphasis

*Italic text*  
_Italic text_  
**Bold text**  
__Bold text__  
***Bold and italic***  
___Bold and italic___

### Edge Cases for Emphasis
* Italic with spaces *  
** Bold with spaces **  
*** Bold italic with spaces ***  
*Nested **bold** in italic*  
**Nested *italic* in bold**  
*Mismatched *emphasis**  
*Multiple***asterisks****  

# Links

[Google](https://www.google.com)  
[Link with spaces](https://example.com/with spaces)  
[Link with parentheses](https://example.com/(parens))  

### Edge Cases for Links
[Link with no URL]()  
[](https://example.com)  
[Link with special chars &<>"'](https://example.com/special&<>)  
[Unclosed link](https://example.com  

# Images

![Alt text](https://example.com/image.jpg)  
![Alt with special chars &<>"'](https://example.com/image.jpg)  

### Edge Cases for Images
![No URL]()  
![][https://example.com/image.jpg]  
![Unclosed alt text(https://example.com/image.jpg  

# Lists

## Unordered Lists
- Item 1  
- Item 2  
  - Nested item  
- Item 3  

## Ordered Lists
1. First  
2. Second  
3. Third  

### Edge Cases for Lists
- Mixed markers  
+ Plus  
* Asterisk  

- Item with multiple paragraphs  

  Second paragraph in same item  

-  
+ Empty items  
*  

1. Out of order  
3. Third  
2. Second  

# Code

Inline code: `code here`  