# tickle
A reminder command-line utility based on the ideas behind [big ass-text files](http://www.43folders.com/2005/08/17/life-inside-one-big-text-file) and the [tickler file system](http://wiki.43folders.com/index.php/Tickler_file).

The tickle command will scan a text file for special reminder commands that will trigger, on the specified dates, the creation of a new reminder or action item.

    tickle todo.txt

For example, the following would create a grocery shopping reminder on August 18, 2017.

    #tickle on 2017-08-18 say A loaf of bread, a container of milk, and a stick of butter. @shopping
    
 The reminder is placed before the tickle command in the text file.
 
    A loaf of bread, a container of milk, and a stick of butter. @shopping
    #tickle on 2017-08-18 say A loaf of bread, a container of milk, and a stick of butter. @shopping
    
This allows for simple searching and management with text editors or command-line utilities.
