Good afternoon and welcome to my talk: "Django as a Database Documentation Tool: The Hidden Power of Model Comments."

I'm Ryan Cheley. I'm a member of the Django Commons admin team with Daniel, Lacey, Storm and Tim, some of whom are in the audience today. I've been a navigator for Django Not Space, and if you're interested in that or want to learn more, session 5 is coming up. There are several people from that community here today. I encourage you to reach out to them. I'm also one of the maintainers of Django Packages with Jeff and Maksudel. I have been using Django for about seven years, Python for about nine years, and I have been in healthcare for 17 years. Some of the things I'm going to talk about today relate to my experience working in healthcare in the United States.

And so why this talk? Why now? I believe in the importance of documentation and extending that to the databases where our data lives. And quite honestly, this allows for better communication between teams within a department or teams within different departments as well.

I'm going to go through a dramatized scenario of what a typical Slack conversation might look like to show some cross-team confusion that could happen from the addition of a new field in a model.

Our web developer posts to Slack: "I just pushed the new model field CHADS score to the patient risk model." And this looks pretty innocent, right? Like we just added a field. No big deal.

But then the ETL developer chimes in and is asking about: well, what does this actually mean and what is it used for? I'm going to have to document this in our data warehouse. And the report developer also needs to know what this is because someone had been asking about adding this specific field to a dashboard, but they don't really have all the information they need to make an effective dashboard.

And so our pain starts here because the ETL developer is blocked from being able to add this field to the data warehouse, which is then blocking the report developer to be able to use that field in the data warehouse.

And so some time later, as the initial web developer consults their notes, reaches out to a business analyst, or finds the subject matter expert that they had been working with to get this field added, they finally have an answer. They come back and they say: "It's the CHA2DS2-VASc stroke risk score."

But we still have a pain point here. We had to wait a while, maybe it was three days, maybe it was three minutes, probably somewhere in between, but we still don't really know what this field is for.

And so there's a real cost here, right? Our ETL pipelines are being delayed, our report development is blocked, and the web developer spent some period of time trying to get an answer for the ETL and report developers and came back with a definition which wasn't helpful and it actually distracted them from working on the next thing that they needed to work on. So here, it's not just a minor inconvenience.

So let's take a look at a current state of what a table might look like. So this is SQL that you might see in PostgreSQL for a table creation, and it's clean, right? Everything is very well laid out. It's functional. It will create the table that you need, but it's completely opaque in its field naming convention. I mean, just look at these field names: HAS-BLED score, QRISK3 value, contraindication flag, and the field that we had just added, the CHADS score. Now, I'm not sure what any of these mean. And someone with direct database access is going to have no clear indication as to what any of this is going to mean.

So we have these mystery fields, and that's really the root of our problem. The database, when the table gets created, has no context about these fields, no business context.

So I'm going to show, this next slide is going to show something that some people may know about but others may not. How many people knew the database fields could have comments in them? Let's see, here we've got CHADS score as the field name and then right below it an empty comment field. Okay, so of you that knew about it, keep your hands up. How many of you have ever actually seen anything in those comments? Yeah. So we have a documentation gap here, right?

So why don't traditional documentation approaches work? Well, code documentation is not database documentation. Those comments aren't going to be in the database, or those comments are not going to be in the database fields themselves.

Any documentation we have outside of our code, in a wiki, whether that's Confluence, or whatever you might be using for your knowledge management system, can get stale, right? Someone adds a new field, but they forget to update the documentation.

You could have this undocumented expertise that exists, right? But that doesn't scale particularly well. If your answer to the question "What does CHADS score mean?" is "Just ask Sarah, she knows," well for a couple of people, yeah, maybe everyone on the team knows who Sarah is. But as your team gets larger, you might have more than one Sarah. And even if you don't, you have a single point of failure here. "Oh, we can't actually find anything out. Sarah is on vacation for the next three weeks. When she gets back, we can ask." These are not super great outcomes to this particular problem.

And in healthcare, and I'm sure in other sectors as well, there's a regulatory compliance aspect to this as well. Our auditors want to know what it is that we're collecting about our patients. They want to be able to look at these fields and know what the definitions for them are.

And I can hear you asking out there: "Well, Ryan, we have this help text. The help text is amazing, right? The help text can tell us all sorts of things about the field, potentially." The problem here is that help text doesn't really solve this because, as you might know, the help text only exists on the front end if we expose it or on the Django admin. The help text is for end users, right? It's for the people that are doing the actual data entry. It's UI-focused guidance. And as I said, it's only visible in forms.

A database administrator in pgAdmin may or may not have access to the front end, and even if they do, they may not know where to go inside of the front end. A data analyst that's using a visualization tool of some kind, like Power BI or Tableau, again, may not have access to the front end and again may not even know where to look. Similar for an ETL developer building our data pipelines. They will never see this help text, most likely.

And so it's at this point we should acknowledge that the help text is a good tool, but for a different audience. This is what the help text might look like on our CHADS score. It says that it's a score for stroke risk assessment that goes from zero to nine with a higher score indicating a higher stroke risk.

So I think we can all acknowledge at this point that we have different audiences who have different needs. Our end users want form guidance and the help text would be amazing for them. Whatever other solution we implement to get context to the database is not going to be important for them.

Our web developers are going to need to know the field's purpose, and so the help text might be helpful to them, but again, it's going to mostly provide tips on any sort of field validation that they're probably going to want to implement. Any commentary in the database would be helpful for them.

Our database administrators want to know about the schema. The help text, they may not even know what forms it lives on, so that's not going to be helpful, but something that lives inside of the database would be.

Our auditors need to know about things from a compliance perspective. The help text might be useful for them if they have access to the front end, but if they don't, or again, they're not sure where to get it from, the context in the database would be most helpful.

And finally, our data analysts who need to have context around these fields: What's the business logic behind some of these things? Why are these important? What would we want to report off of? What would we want to visualize for these items? The help text again, not going to be great, but something else inside the database would be.

And so we can see where the help text falls short, right? Our data team that's using Power BI or SSRS or Tableau or any one of a number of different visualization tools can't see the help text. Our regulatory auditors are not going to be able to look at the front-end necessarily or the Django admin necessarily, but they might, but they will be looking at the database directly. And cross-team collaboration, as we saw before, our ETL developers are delayed in pipeline completion which then impacts the report developers being able to create the visualizations and dashboards that they're working on, which also impacts the web developers who originally created and added the field to the model because they had to go back and research what it is that field is actually for.

But in Django 4.2, which was released on April 3rd of 2023, we got this new parameter on a field called db_comment. A quick show of hands, how many of you have actually used this before? Okay, great.

And this is what it looks like inside of our model. It looks very similar to what we had seen before with help text, but now we've got more context behind it. This isn't UI guidance, this is information about the field itself. We can see it's a stroke risk that goes from 0 to 9, where a greater than 2 indicates anticoagulation consideration based off of ESC guidelines from 2010. Wow, I now have a lot of information about this specific field.

And what this will actually do, as we'll see later on, is it will allow us to put documentation directly into the database schema. And I want to call out just how clean this is, right? There's just a narrative sentence in this db_comment on the field that we're talking about.

And the magic happens—I think it's magical—when the migration occurs, because it will put this comment directly into the database where anyone with database access can actually see it. And so we finally have a solution to our original problem, which is the documentation about this field is going to live inside the database.

And so what this might look like from a SQL perspective is that we are altering our table to add the column CHADS score as an integer not null. In addition to that, we're going to put a comment on the column that matches what we put into db_comment. And the result is that anyone with querying access to the database can now see these comments. They now have full context around what this specific field actually means, which is helpful, of course, for reporting purposes, for compliance purposes, for ETL pipeline development purposes.

And if you're using pgAdmin, this is what you'd actually see. If you went and right-clicked on the field CHADS score, you would see the name of it, but then you'd also see that comment that we added to db_comment. And so just to take a step back, before we had these mystery fields, right, where the names might be meaningful but probably weren't.

So let's take a look at a before and after to show how the db_comment can help us here. We have a typical Django model here. It's clean, it's functional, but it doesn't really tell us anything about the fields themselves. The ETL developers, again, no idea what CHADS score represents. Is it a count? Is it a percentage? Is it a risk level? Which means that delays the pipelines, but the report developers also are going to have a challenge here because they can't build meaningful dashboards around these data elements without the context needed from the comments that we would be adding.

And let's be honest with ourselves here as well, even the original web developer who added this field is going to look at this in three weeks, three months, three years, and not really have any idea what this field means. Are you really going to remember what QRISK3 value means? I probably won't.

So let's start adding db_comments and remove the mystery around these fields. We'll look at the CHADS score, and we've added it here to our patient risk model. We have db_comment listing out exactly what CHADS score means, and it gets applied to the database. It's going to be in the comment on the field.

Okay, well what about HAS-BLED score? Great. Well, we've got the comment. It's a bleeding risk where greater than 3 indicates a high bleeding risk per the FDA guidance of 2019. So we have context for anyone with database access. Our ETL developers, our report developers, our database administrators, our auditors. They can now see this information by looking at the comment on the field.

But let's take a look at maybe a little more complex of an example, a JSON field that might have several keys based off of the web front end. Well we can document what those keys are here and we can see that these are going to be used to track clinical contraindications per CMS 134 v8, whatever that means, and the keys we have are warfarin_allergy, bleeding_disorder, and pregnancy_status, and these will be boolean values. So now we know everything we need to know about this specific JSON field. We know what the keys are and we know that they're always going to be true or false.

And now the ETL developer can look at this and they know the JSON structure without having to go digging through all of the different values that might be in the table. They can turn these keys into unique columns for reporting later on that can ease report and dashboard development for those report developers.

Okay, great. So we have added documentation to our database that has meaning for our contraindication flags. But does that mean that I shouldn't do the help text anymore? No, not at all. We can have both features working together. We have the help text on our field which is going to be for our data entry users, those that are using the front end of our application, and the db_comment that's going to be for our database users. And so I'd say as a best practice, you would want to use both because, again, they serve different audiences.

All right, you might be asking, well, this is super awesome, right? But what about tables? Sometimes tables can get confusing, right? Well, also in Django 4.2, we got db_table_comment for this. You can add your table comments, and it looks a little something like this. In the meta class on your model class, you just add a db_table_comment with text about what the table actually means. And in this case, this table is a cardiovascular risk calculations per the Joint Commission PC-03. And the owner is the cardio team with CardioTeam@example.com as their email address.

And so we have table level documentation. And this is amazing because this tells us what this table is and who the owner of it is, so we have a point of contact about it. And if we want to look at what the comments, what the documentation inside of the table itself in pgAdmin would look like, it would look something like this.

And so now we have full documentation for everyone. Going back to that original table, we've got this db_comment that helps us to understand from a database perspective what these fields mean. We have help text to help the users understand what should be going into those fields.

Okay, hopefully I've convinced you of the awesomeness of db_comment and db_table_comment. But where do you start? Well today you can go and audit your top 10 most confusing fields. Look at cryptic names or fields that have some weird business logic around them. Look back at your retrospectives or maybe you've implemented a new feature and there was a lot of confusion around a specific set of fields. Just find 10 of them. Do the research on what each of those means through your notes, interview subject matter experts, your business analysts, whomever, and write up a helpful, useful comment that you can add to db_comment. And finally, standardize. Update your code review processes to make sure to include db_comment in any new fields that you add. You could also add tests that will fail for any field that doesn't have them already.

Okay, for db_table_comment, a similar approach. You want to audit anything that has happened where there were confusing names or cryptic names, identify owners, and do this for your top 10. I did see a table name called SWPTABTPRNIB. Yeah, so stop there for a second. And you get to your top 10 most confusing tables. So once you've identified them, then you want to start to document them. Go get as much business context as you can, get the owner details of each of the tables and put it into a narrative that can be added to the db_table_comment. And then standardize. Again, updating your processes to include code reviews that are looking for these and that the code reviews will fail when they're not there. You can also add tests.

And this gets you in the habit of making documentation an actual habit instead of just an afterthought, right? So hopefully I've been able to convince you of the power of db_comment and db_table_comment, and that you can make documentation a habit and not just an afterthought. My hope is that we can reduce confusion and that documentation is not just for helping others, it helps our future self as well.

Thank you so much. You can find me at various places online and I'll now take questions.
