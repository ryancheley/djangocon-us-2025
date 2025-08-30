Good afternoon everyone and welcome to my talk, Django as a database documentation tool, the hidden power of model comments. I'm excited to talk to you today about this feature that I believe can change how your teams transform the way that they work with databases.

Hi, I'm Ryan Cheely. I am a member of the Django Commons admin team with Daniel, Lacey, Storm, and Tim, some of whom are in the audience today. I've also been a navigator with Django Not Space, which is going to be starting up session five here at the end of the month, and you have a chance to sign up for it within the next week and a half, I think. I'm also one of the maintainers of Django packages with Jeff and Maksudl. Jeff, who's in the audience today, and Maksudl, I'm sure, is at home watching the live stream.

A brief bit about me from a Python Django perspective. I've been working with Django for seven years now and Python for about nine. And then lastly, I've been in healthcare for 17 years, which is a mind-blowing number for me. And that's going to become important later on in some of the examples that I give.

And so why this talk? Well, I believe in the importance of documentation and I believe that it has a great benefit for communication, both intra-team communication as well as inter-team communication. So within your team and outside of your team.

I'm going to go through a dramatized scenario that you might find in a typical Slack conversation, maybe within a healthcare setting. So the ETL developer posts into the Slack channel that might be shared with some other folks, "Just push this new field CHAD score to the patient risk model." And this looks innocent enough, right? They just are letting everyone know that there's a new field out there. Okay, great.

But then the ETL developer posts and asks, "Well, hey, I need to add this to a risk dimension, but per our policies, I have to know what this field actually means, so I need some documentation. Can you tell me anything about it?" And the report developer says, "yeah, I actually have to use that field that's going to get added to the dimension in a dashboard that I've been asked to update, and I can't do that until ETL developer is blocked."

Right, so here's where some pain starts. The web developer posted a pretty innocuous comment about a new field, but there are now two different teams that need clarification on that field, and they're blocked from moving forward.

And at some point, while the web developer is working to try to figure out the answer to these questions, maybe it's three minutes, maybe it's three hours, maybe it's three days. Because they have to work to consult their notes, maybe they have to reach out to a business analyst. Maybe they have to track down a subject matter expert to answer this very valid question.

And so they do come back with an answer, but the answer is it's the CHA2DS2-VASC Stroke Risk Score. So we had to wait a while to get what is still not an informative answer. It's a risk score for stroke but is there anything else to it? We don't really know.

And so there's a real cost here. There are delays in our ETL pipeline changes and deployments. We have a dashboard that's blocked because it depends on the changes to the ETL pipeline deployment. The web developer just spent some period of time tracking down through their notes or finding a business analyst, a subject matter expert to come back with that fairly opaque answer. So they weren't able to do other things because of this. So this is real loss productivity. It's not just a minor inconvenience.

Okay so let's look at the current state of what our patient risk assessment model might look like. And if you look at it from a straight SQL perspective when you want to do the table creation, it might look something like this. This statement is clean, it is functional, it will create a table for you. It will create a table with all the proper columns that you want and they will have the proper types.

But this is completely opaque. I mean just look at these field names: HasBlendScore, QRISC3Value, ContraIndicationFlags as a JSON field, and our new field, the Chad score. As I said, I've been in healthcare for 17 years and some of these I'm not even sure what they might mean.

And if all you have is access to the database, like direct database access, there's no clear indication once these fields get created in a table what any of them might mean. So this is really the root of our problem. We have these mystery fields that provide no business context when all you might be able to do is look at the database.

And so if we go and look in PG admin, we could look at a specific field and we can see a comment field associated with this chat scored field. How many people knew that fields could have comments inside of PG admin or really any database? Okay. Keep your hands up. How many of you have ever seen that actually filled in?

Right, so not everyone knows about it, and those of us that do rarely see it filled in. And this leads to a documentation gap. I think we all maybe know, or at least understand, that comments in our code are not the same as database documentation. Wiki pages that might attempt to provide full business context around fields can get stale. You update a new field or you update a table to add a new field but you forget to update the wiki.

You might have a sense of this undocumented or undocumented expertise - "Just ask Sarah, she knows." But this doesn't scale well. It offers up single points of failure. And as your team gets larger, you might have more than one Sarah. And so the statement, "just ask Sarah, she knows," starts to lose meaning. Which Sarah are we talking about?

And in healthcare, we are a regulated sector. We have auditors, and those auditors want to know what these fields are. And so having this documentation in the database can be very helpful for that.

And I know what you might be thinking out there, "but hey, Ryan, we've already solved this problem. We have help text. That'll tell us everything we need to know." But it doesn't actually solve the problem.

Because you see, help text is for end users. It's for the people that have actual access to the front end application, or maybe the Django admin. It's to help them put data into the database. It's UI focused. It is not meant necessarily to be the thing that tells someone who is consuming the data from the database what that data actually means.

And again, this is only available in our front-end forms. It's not going to be in PG admin in the comment like we saw before. It's not going to be available to a data analyst or a report developer who's working on a visualization tool using Power BI or SSRS or Tableau. It doesn't help our ETL developers build data pipelines. They're never going to see this help text. And even if they could see the help text, they may not be able to map that field on the front end to where it exists in the back end.

So we have a good tool, but for the wrong audience.

And so here's just a quick example of what some help text might look like for the CHAD score. It's the CHA2DS2VASC score for risk stroke assessments, and it goes from 0 to 9. Higher scores indicate a higher risk score, a higher stroke risk.

And so it's at this point we should probably acknowledge that we have different audiences, different stakeholders who have different needs. We've got end users who require form guidance, in which case the help text is going to be just that, helpful. Are they going to care about any comments that might exist in a database? No.

Our web developers are going to want to know about the field's purpose. And so the help text, yeah, it's helpful, but any comments on the database would also be helpful.

Our database administrators want to know about the schema of the database. So the help text, they're not going to find too much assistance in that, but anything that's in the database itself would be very helpful for them.

In a regulated industry like healthcare, auditors are going to want to know about compliance related things. And so the help text might help them if they can find the front-end version of it, but really what they're going to want are the comments around the fields of the database.

And finally, our data analysts. They're going to want to know the context of the database itself. And so the help text, they're probably not going to find the field that they're looking for on the front end anyway, even if they have access to it. And so, again, a comment in the database is going to be the most helpful.

And so we can kind of see that help text falls short here. It's not helping the data team that's using SSRS or Power BI or Tableau to create visualizations. They can't see the help text, and even if they can, they might not be able to map what they're seeing on the front end to that field in the back end.

It doesn't help with regulatory audits. The auditors may not have access to the front end or to the Django admin. They might be looking directly at the database itself. And going back to our original pain point of cross-team collaboration, the web developer posted about a new field, but the ETL developer and the report developer both didn't really know what it meant, what the proper definition of it was for. So there's no proper context for them there.

But this all gets fixed with db_comment, which was introduced in Django 4.2. For those of you who aren't aware, Django 4.2 was released in April of 2023, a little more than two years ago. So I am wondering, how many of you have actually used this feature? Okay. All right. Awesome.

And so with this DB comment, we can see now on our CHAD score, we can add a very meaningful comment about what this field is. It's the risk stroke score. It goes from zero to nine, with two being an indication of anticoagulation consideration based off of 2010 ESC guidelines.

And so this actually puts documentation directly into the database. And notice how clean this is. Nothing fancy that had to be done here. It's just a new attribute of the field, much like help text. And the magic happens with the migration in that it puts this comment directly into the database where anyone with database access can actually see it.

So we have a solution with db_comment. The documentation lives in the database itself.

And so if we go back to the migration itself and the SQL that it might generate, well, it's going to alter the table in the case of the CHAD score by adding the column, making an integer. It's mostly straightforward SQL. But it also adds a comment on the column, which matches the db_comment that was added in the model itself.

And as a result, we now have a comment in the database that allows anyone with direct database access to see exactly what that field is for. And here's an example of what it looks like inside a PG admin. We now have this comment, and it's filled in!

Before, we had these mystery fields. Has led score, QRISC3 value, Contraindication flags, the CHAD score. So now let's start adding DB comment to see how this would help.

I mean, this is a typical Django model. It's clean, it's functional, but it doesn't tell us anything about the fields themselves. Again, ETL developers, which just based off of this information are going to have no idea what a CHAD score represents. Is it a count or a percentage or a risk value? And let's be honest here, the web developer that added CHAD score in three weeks, three months, next year, they're not really going to remember what this field means either.

So let's start adding some DB comments. And again, we added to CHAD score, we can see this comment is going to be added to the comment in the field in PGAdmin.

But what about the HasBled score? It's another confusingly named field. It's a bleeding risk based off of FDA guidance from 2019. And so now by adding this DB comment, we actually have context for our ETL developers, for our report developers, for our data analysts, for our auditors. Then again, the comment goes directly into the comment section of the field inside of PGAdmin.

One of my favorite examples though is some more complex ones: JSON fields. JSON fields that have multiple keys. What are those keys? I don't know. But now, by adding a DB comment, we can actually state what the possible keys in that JSON field are.

And why does this matter? Well, the ETL developer is going to get to see that comment, as we'll see in a second, inside of PGAdmin. They'll know what keys are there. They'll know what possible values of those keys could exist. In this case, we have the keys of Warfarin, Bleeding Disorder, and Pregnancy Status, which are Boolean values. Now, they can take this JSON field and turn it into, potentially, attributes of a dimension that are based off of these keys, which makes report development easier because all they're doing is looking at the keys of the attributes themselves and not having to extract out the JSON every time they write a SQL statement.

And so again, here we can see inside of pgAdmin in the comment. Now we have this database documentation that provides full meaning on what this exact contraindications flag actually includes.

Okay, so should you use both fields? Should you use one over the other? I would say you should use them both together because they serve different audiences. The help text is for data entry, for those people to have access to the front end. The db comment is for our users that have access to the database directly. So I'd say as a best practice, you should use both because again, they serve different audiences.

Okay, well, but what about tables? Sometimes you come across weird table names. Is there a feature that would allow me to be able to do this on tables? And yes, there is. Also introduced in Django 4.2 is db_table_comment, which allows you to add a table comment.

And so by adding a meta class to your model class, you can fully describe what that model is actually about. And in this case, our patient risk model is cardiovascular risk calculations based off of joint commission PC-03. The owner is CardioTeam, who are available at cardioteam@example.com.

So we get table level documentation here. We have a what this table is about, and we have a who as the owner for the table. That means that if there are questions, if something goes wrong, whatever, you know who to contact about this specific table.

And this is what it will look like inside a PG admin. Again, not sure if anyone has ever seen or knew the comments were available on tables, and if they did know about it, had they ever seen something actually filled in there.

But now we've got full documentation for everyone. Our end users have form guidance based off of the help text. Anyone who needs to know about the backend fields themselves has it directly inside of pgadmin.

Okay, hopefully you're on board with wanting to implement this, but where do you start? Well, I think it's relatively straightforward. Identify the top 10 most confusing fields in your project. Look for cryptic names or complex business logic. Maybe go through your retrospectives from the last six months and what were the things that had the biggest challenges from an implementation perspective or the thing that introduced the most number of questions after deployment. Get 10 of those.

Start documenting. Start adding, start writing up a comment that could be added to db comment. Include business context and logic and especially compliance notes that could be helpful later on for your auditors.

Last thing is just standardize. Make this a part of your common practice. If you have code review templates, checklists, whatever it is, make this something that you just do as a part of the introduction of new fields.

Similar to the DB comment, for DB table comment, again, audit. What are the 10 most confusing table names, models that you have introduced or seen? Start researching. What are these models used for? Who are the owners of them? What specific business logic might be involved with them? Are there any compliance related issues that should be documented in here? And again, standardize your review process. Make this a part of the thing that you do when you introduce a new model.

You could, for both of these, add failing tests when these are missing. This allows you to make documentation on your fields and your tables in the database a habit and not just an afterthought.

Hopefully I've been able to convince you of the power and usefulness of db comment and db_table_comment and that you can make this documentation a habit probably in the same way that you made docstrings a habit and not just an afterthought.

Thank you so very much. My hope is that you can take this db_table_comment and db comment, take it home, apply it to your tables to help reduce confusion amongst your teams to help increase documentation that will help not just your fellow co-workers, but you as well with documentation. You can find me in various places online and I look forward to your questions now. Thank you so much.
