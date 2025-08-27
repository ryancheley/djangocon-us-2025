Good afternoon everyone and welcome to my talk Django as a database documentation tool the hidden power of model commons. I'm excited to talk to you about this simple but powerful Django feature that can transform how your team works with databases.

A brief introduction, my name is Ryan Cheely. I'm a member of the Django Commons admin team with Daniel, Lacey, Storm, and Tim, some of whom are in the audience tonight. I've also been a navigator in Janganaut space. For those of you that are interested in Janganaut space, either as being a mentor or participating as a Janganaut themselves, session five is coming up, and I highly recommend you take part in this particular program. It's an amazing opportunity.

I'm also one of the maintainers of Django packages with Jeff and Maksudel. Jeff is in the audience. Hey, Jeff. I've been working with Django for about seven years and Python for about nine. These two numbers kind of blow my mind, quite honestly, when I think about them. The number that really blows my mind, though, is that I've been in healthcare for 17 years. And that'll come into and make a little more sense later on as I go through some of the examples that I have.

So why this talk and why now? Well, I believe in the importance of documentation and the great benefits that it can have for inter-team communication as well as intra-team communication. And so I'm going to go through a dramatized scenario of something that could happen.

And we'll look at a typical Slack conversation. So a web developer posts in the Slack channel, hey, it just pushed a new field CHAD score to the patient risk model. This looks innocent enough, right? Okay, great, a new field. Sure, whatever. But then the ETL developer says, hey, you know, I actually need to add that to the data warehouse. I need to make sure that it's fully documented. Do you know what this field means?

And then the report developer chimes in and says, yeah, and I've been asked to add this field to a visualization or a dashboard, but I can't add that data until the ETL developer gets what they need from a documentation perspective. And so this is where the pain starts, right? The ETL developer has needs to get documentation. The report developer has needs to get that field in to the data warehouse so they can provide a visualization. And they're both blocked for clarification.

And so they've asked their questions and sometime later, maybe three minutes, maybe three hours, maybe three days, the original web developer goes back, they consult their notes, maybe they reach out to a business analyst and ask them for some clarification on the field. Absent that, perhaps they reach out and find a subject matter expert who can help to answer the question, what does this field mean?

And after all that time, they come back. And the web developer says, it's the CHA2DS2-VASC stroke risk score. Wow, we waited a while to get that answer, and we still don't really know what it means.

And there's a real cost here, right? The ETL pipeline deployment and updates are delayed while we're waiting for this information so that it can be well documented. The report developer is blocked because they can't actually enhance their dashboard or visualization until the ETL developer can add the field with the proper documentation. And the web developer has lost productivity going back and looking through their notes or finding a business analyst or a subject matter expert who both lost productivity to help answer this question. So this is a real impact, right? This isn't just some minor inconvenience.

All right, let's take a look at a current state of what our patient risk model might look like today from a SQL perspective. It's pretty straightforward, right? It's clean, it's functional, we know what the table is called, we know what all of the field's types are, we know what the field's names are. But this is completely opaque, right? I mean, just look at the field names: Hasbled score, QRISC-3 value, contraindication flags, how many of those are there, and then our new field CHAD score. Some of these I'm not even sure what they mean. And remember, I've been in healthcare for 17 years.

And so if you only have direct database access and this is all you see, there's not any clear indication what any of these data elements are for. And so this kind of gets to the root of our problem, right? We have these mystery fields. What do these names mean? The database itself contains no business context at this point.

And so I want to take a look at PGAdmin. How many of you knew that database fields could have comments in PG Admin. Okay, great. Keep your hands up. How many of you have ever seen those comments filled in? Right. So, there's a gap here, right?

Why don't traditional documentation approaches work? Well, as we all maybe know, code comments, that is, comments in our code, doc strings, those kinds of things, are not the same thing as database documentation. Try as we might to keep our wiki pages or our confluence pages or whatever knowledge management system you and your team or your company use, they can get stale. Someone pushes an update to code, but they forgot to update the wiki article.

Undocumented expertise doesn't scale. And what do I mean by this? I mean the, oh, well, if we're small enough, just go ask Sarah what this is. She knows. But as your team gets larger, I might not know who Sarah is, or there might be multiple Sarahs. So which one do you ask? And then no one seems to know what the right Sarah's last name is. So we have single points of failure.

And from a healthcare perspective, we've got healthcare and regulatory requirements that in some cases, the auditors want to see what data we're collecting inside of our databases and what it means.

And so you could rightfully be out there in the audience right now saying, "Well, hey Ryan, we've already got a solution for this. It's called HelpText, right?" And here we can see what HelpText looks like on the CHAD score. And it says enter a score of zero to nine based on patient risk factors.

But I'll argue the help text doesn't actually solve this problem because where is the help text? Well, it's going to be in the user entry form on the front end of the application or in the Django admin, two places that back end data analysts, DBAs, auditors may not likely won't have access to.

And so this is where we can kind of think about, Well, the help text is really for UI-focused guidance, right? As I said, it's only visible in the front-end forms. It's not available in PGAdmin in the comment section that I showed you before. And anyone who's trying to use a visualization tool or create an ETL pipeline is likely not going to see this text. So it's a good tool, but for a different audience.

And just as a reminder what the help text might look like in a user entry form, we can see, well, here's what the score looks like or what the help text looks like in our form.

And so it's at this point we need to acknowledge that we have different audiences, different stakeholders that have different needs, right? So our end users need form guidance. They need to know what values can and should be entered into these fields and maybe a little bit about them. You'll obviously want to have some validation on these fields, but the help text is there to help the data entry people put in the right data. So help text, yes. Something that goes in the database, maybe not so much.

Our web developers are going to need to know what the field's purpose is, right? So the help text could be helpful for them, but something in the database would also be very helpful for them. Our database administrators want to know about the schema, the help text they may never see. So that comment in the database is going to be very, very helpful. And our auditors who are looking at this data from a compliance perspective, maybe they can use the help text, maybe they don't have access to the front end or Django admin, so data comments are going to be very helpful for them.

And finally, our data analysts, the people that are taking the data out of our systems through an ETL process into a data warehouse of some kind, they need to know the context of what these fields mean, why they're important, who to ask questions of. The help text isn't going to get that for them, but something in the database would.

And so again, where does the help text fall short? Well, for a data team or report development team that's using a platform like SSRS, Tableau, Power BI, any one of a number of different things, they may not be able to see the help text because they can't access the front end or the Django admin. Our regulatory auditors, again, they are going to not be having access to the front end potentially, so you've got to have somewhere where they can see this documentation. And cross-team collaboration. As we saw before with all of that confusion around the addition of the CHAD score and the amount of extra effort that needed to go into getting everyone up to speed on what that new field meant, there was a lot of time lost there.

And so in Django 4.2, which was released in April of 2023, we got this fantastic new feature called DB comment. A quick show of hands. I'm wondering how many people have used this before in one of their current Django projects? Okay. All right. Awesome. A couple of you out there. Well, hopefully I can convince you that this is an amazing feature that should be used everywhere.

So let's take a look at what this DB comment might look like on this CHADS score. We now have a little more context here. It's the CHA2DS2-VASC stroke risk from 0 to 9, where greater than 2 indicates anticoagulation considerations per the 2010 ESC guidelines. So this puts the documentation directly in the database schema for those that have direct database access to see, to appreciate, to learn from.

And just kind of notice how clean this is, right? We just add a simple attribute of db underscore comment with the comment about the field, and the rest takes care of itself through the magic of Django migrations. Because it's going to take this comment and put it directly into that comments field that we saw earlier, and we'll see again, where anyone with database access can see it.

So now we have a solution where the documentation about the field doesn't live in a code comment, doesn't live in a help text, it lives in the database itself. And what you might wonder is, well, okay, great, so we add that, and then how does that look from a SQL perspective? Well, we have the alter table, which is going to add this column of chad score, but it also adds this comment on column and it takes the comment that you put into db_comment and adds it as a comment through the SQL. And as a result, again, anyone with query access to the database can see the documentation.

And if you're using pgadmin, this is what it would look like. You can see the exact comment that was in the db_comment from the field itself.

And so before we had these mystery fields, right? HasBled score, QR3 risk, or QR, QRISK3 value, contraindication flags, CHAD score. But again, we don't really know what any of these necessarily mean.

So let's see how DB comment can help us. We're going to take this typical Django comment, which is clean and functional, clean and functional, but doesn't tell us anything about the fields themselves. And we're going to start adding some context here. Because again, in looking at this, an ETL developer, when these fields get pushed out to the database, may have no context behind it. What does the chat score represent? Is it a count or a percentage, a risk level, something else entirely? Which means that after all of the digging to get this information and if they're able to add it to the database, it makes it more challenging.

So we have this problem, but let's start adding DB comments. Again, taking Chad's score. We'll take the data that we have discovered about what this field actually means, that it's a risk score from 0 to 9, and it goes into the database, into pgadmin. A similar thing for the Hasblad score. In this case, it's an indicator of bleeding risk from 0 to 9, with greater than 3 indicating a high bleeding risk based on FDA guidance from 2019.

And so now we start having these self-documenting models, which gives context for the ETL developer, for the report developer, for the auditors. And we can see now the comment gets into the comment section, the DB comment gets in the comment section of PGAdmin, just like we saw with the CHAD score.

I think one of the more interesting aspects of this, though, is when we start talking about JSON fields. Because now we can start to take some of that complexity that we can wrap up into a JSON field and actually start talking about the keys that are there. In this case, contraindication flags has three different keys in it. Warfarin Allergy, Bleeding Disorder, and Pregnancy Status. And they're all Boolean values, either true or false.

So with this, the ETL developer knows the JSON structure without having to go spelunking through the Django code to figure out what possible keys could be there. And if the opportunity is right, they can take these keys from that JSON field and expand them out into specific indicator fields inside of a dimension that can then later be used by the report developers, which can ease report and dashboard development.

And so this is what the comment that we saw before might look like inside of PGAdmin. Again, it explicitly states the keys that provides meaning to our database and allows those with direct access to really appreciate what's in these fields.

Okay, so now I've hopefully convinced you about how awesome DB comment is. You might ask, well, does that mean I shouldn't use help text ever again? Well, no, no, I still think you should. These features work together. The help text is for the data entry users, the people putting the data into the database. The DB comment is for the people who are consuming data from just the database and maybe don't have access to the front end. Or even if they do have access to the front end, they may not actually know where to find that specific field in the front end application.

So I would say as a best practice, we should use both. Because remember, we have different audiences and we should serve the intended audiences of those different features.

Okay, great. So this is awesome, but what about tables? Can I do the same thing for tables? And yes, you can, because also in Django 4.2, we introduced db_table_comment, which allows you to add a table-level comment from your Django code into the database.

And so when we look at it, we add a meta class to our model class with a dbtable comment, and we just list out the documentation for it. In this case, we have cardiovascular risk calculations for the Joint Commission, and that the owner of this specific table is the cardio team, who have cardio team@example.com as their email address. So we have a "What is this table for?" and we have a "Who are the owners of the table?" Provides a full picture of context about this specific table.

And this is again what it will look like inside of PGAdmin. We can see there's the comment about this specific table, allowing those with direct database access, the context and documentation they need in order to move forward with the tasks that they've been assigned and to solve the problems that they need to solve.

So we've got full documentation for everyone by using both the help text and the DB comment. The end users get the form guidance that they want and need, and the direct users of the database have those comments that they want.

Okay. Where do you start? You can start today with three simple steps. Step one: just audit. Identify the top 10 confusing fields. Now 10 might not seem like a big number. Maybe it is, maybe it isn't. But once you get into a rhythm for how to identify the fields and go through the next steps, you kind of want to start small because you're going to figure out your own rhythm, your team's rhythm for making this the best process that it can be.

So once you've identified your top 10 confusing fields, start documenting. Do the research. Go back through your notes, find the business analysts, the subject matter experts, whomever that can help you in providing details and distill those details down into the best DB_comment you can.

And then next is standardized. Once you've gone through the 10, you'll have a good sense of how this works. Just make it part of your standard practice. Your code reviews, any checklists that you have for when you're implementing new fields, new models, just make it a part of your practice and then suddenly you'll have hundreds of these.

And same with DB table comment. Audit your 10 top confusing tables or models. Look for cryptic names of tables that maybe you don't honestly know what they even mean anymore. Fun fact, there was an email that sent to the technical team that I was on that was talking about not a table, but an acronym, which was SWPTABTPRNIB. Which, who knows, maybe that gets put into a table at some point as a model name and then no one knows what it means. I happen to know what that means only because I had the great opportunity to hang out with a whole bunch of really awesome clinicians. And so when I saw it, I knew that it meant spoke with patient about taking ibuprofen as needed. How many people are going to know that, though?

Again, once you've audited your tables, start documenting. If you do this right, you're only going to have to do it once. So spend the necessary time to do it. It will really reap rewards from it later on. Add details about the context. Add details about the business owner. Whatever it is that's going to make your life and the lives of your ETL developers or anyone with direct access to the database easier in the long run.

And then again, standardize. Update your code review process to make sure that each of your new models has this DB table comment added to the meta class. You're striving to make documentation of these fields, of these models, a habit, not just an afterthought.

So, hopefully I've convinced you of the power and usefulness of DB comment and DB table comment and that you can make documentation a habit and not an afterthought. Thank you so much. I hope that my talk will help you to reduce confusion amongst your team, that you'll know that documentation helps not just others, but it also helps you in the future.

You can find me in various places online and if there are any questions I'd love to hear them now. Thank you so much.
