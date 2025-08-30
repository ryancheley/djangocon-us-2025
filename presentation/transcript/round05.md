Good afternoon, everyone, and welcome to my talk, Self-Documenting Databases. My name is Ryan Cheely. I am a member of the Django Commons admin. I've been a navigator in Djanganaut space on three different occasions, and I'm one of the maintainers of Django packages with Jeff and Maksudel. I have eight years of experience with Python, seven years in Django, and I want to give this talk because I believe in the importance of documentation and the great benefit that it can have on intra-team as well as inter-team communication.

So I'm going to walk through a real-world scenario from where I work. I want to show you what happens when developers add a new database field without proper documentation.

Here's a typical Slack conversation that can happen. A web developer posts in Slack just pushed up a new field, Chad Score, to the patient risk model. Looks innocent enough, right? But then the ETL developer comes into the Slack channel and says, hey, this is great, but I need more about this particular field in order to add it to our risk dimension table. Like, what is it? What does it calculate? And then the report developer adds in that they also need this for a new dashboard, and they need the dimension specs before they can proceed.

And this is where the pain starts, right? Multiple teams, the ETL team, the report team, are blocked waiting for clarification from the web development team. And so some period of time later, maybe three minutes, maybe three days, the answer comes back. The web developer says after consulting their notes, following up with the business analyst, or consulting a subject matter expert? Well, it's the CHA2DS2-VASc stroke score risk. Great. We had to wait a while to get that answer, but I don't know if we're any closer to actually knowing what this thing means yet. We just have a textbook definition.

And so there are real costs here, right? There are delays in the ETL pipeline deployment because they're waiting for field clarification. There are delays with report development because they're waiting on requirements for the dimension. And there's a developer productivity loss here. As I said, the web developer was asked by the ETL developer and the report developer what the field meant, and maybe they have notes that explain it, and maybe they don't. And if they don't, and there's a business analyst, maybe the business analyst has it, maybe they don't. So then they have to go find a subject matter expert to try to get this information from.

So let me be clear, there is a real impact here, right? All development teams have suffered productivity losses here because they were blocked or they had to go find an answer from someone, which then blocked them from doing other work.

So let's take a look at the current state of what our database table might look like today. And here we can see that pretty vanilla Postgres with a patient risk assessment table being defined by these specific fields. We have an integer that's also a primary key for ID. There's a HasBled score, which is an integer, a QRISC3 value, which is a decimal, a contraindications flag, which is a JSON field, and this new field, the CHADScore integer, which was just added.

And you can look at these names and maybe if we have some context into what these fields might actually mean from a healthcare perspective, you know what it is that they actually talk about. But if you're not, you likely look at these and have literally no idea what any of this means. Now imagine that you're a database administrator and you come into a table that has this structure in it, they'll have no idea what these fields are or even why they matter.

So we have these mystery fields, these cryptic names that don't actually mean anything necessarily outside the domain expertise of where this is drawn from. And this is the root of our problem: the database itself contains no business context.

When you actually look inside of Postgres, you might see something like this on the score and you'll notice something here underneath the name chat score it says comment. Now how many people in here actually knew that fields in a database could have comments? Now how many of you have ever seen those comments filled in?

So there's a documentation gap here. You might ask well why don't traditional documentation approaches work. Well, code comments are not database documentation. Code comments are great for when you're actually developing and reading the code that was written for the application itself, but they don't help DBAs or data analysts or anyone with direct access to the database know what the fields mean.

And wiki pages or Confluence pages or whatever you want to call them, they can get stale quickly. Someone updates the code but forgets to update the documentation. There's also this idea of undocumented expertise. The just ask Sarah, she knows approach. And that doesn't scale particularly well for a couple of reasons. It creates a single point of failure. "Well, Sarah is on PTO for the next three weeks. I guess we'll never know until she gets back." Or, "Which Sarah? There's more than one." And you'll always end up asking the wrong one the first time.

In healthcare where I work, we have regulatory requirements where auditors need to see field-level documentation to understand what data we're storing about patients.

But you might ask, what about the help text? We can add help text, which we can see right here, but the problem is that it is limited because it doesn't help solve the problems of those that have direct database access. Help text is, as you may know, designed for end users filling out forms. It's UI-focused guidance, not database-driven guidance.

The other issue here is that it is only available to those users who are looking at those fields in the data entry context, either of a front-end application or maybe the Django admin. The help text does not populate in those comments that we saw earlier in, say, PGAdmin, or for the data analyst that is trying to get context around this.

So if you're a DBA using PGAdmin or a data analyst using Tableau or an ETL developer building data pipelines, you'll likely never see this help text. It's the right tool for the wrong audience.

Here we can actually see what the front end might look like where the chat score has the definition below it and tells the user what it is that they should be doing, but none of this information is going to make its way into the back end, into the database.

So it's at this point we need to acknowledge that different audiences have different needs. Our end users need form guidance, and the best thing for form guidance is going to be the help text. They're probably never going to see the DB comment. Our developers need to know a field's purpose, and so the help text could be helpful, but a DB comment will probably be more helpful. Same for our DBAs, they need to know about the schema. Again, help text, not so much, DB comment, for the win.

Auditors, from a compliance perspective, probably not going to see the front end, probably not going to see Django admin, and even if they could, the help text won't give them what they actually need, that's going to be in a DB comment. And finally, our data analysts, our report developers, whoever it is that's actually consuming this data for downstream purposes, need to have database context. Again, the help text is not so helpful. What they need are database comments.

We're talking through here and we can see where the help text falls short. The data team using SSRS or Power BI or Tableau, they're not going to see the help text. In a regulatory audit, the auditors are examining the database directly and not necessarily any of the front-end applications. For cross-team collaboration, ETL developers building dimensions are not going to have field context here if there's no DB comments.

And so in Django 4.2, which was released in April of 2023, we get DB comments. Now we can add this DB comment with more context behind what the field actually is. Here the DB comment is quite specific, giving a range of values from 0 to 9 for the CHAD score, letting you know that a value greater than 2 indicates anticoagulation considerations and it's based on guidelines from 2010.

Now this is where the magic happens because when Django generates the migration, it puts this comment directly into the database where anyone can see it. And that means that documentation lives in the database itself.

What this generates is the things that we're used to seeing here with the CHAD score. But it also adds a comment on the column itself that shows the actual data, the actual comment about what the field is. Which means that anyone querying the database can see the documentation.

If we go back to PGAdmin, we can actually see this comment in the database. It got there through the migration, through the use of dbcomment.

So before with the mystery fields, ETL developers and report developers, data analysts, DBAs have no idea what the fields represent. And let's be honest, even the web developer that worked on it in three months or six months is not the same person who worked on it today, and they will likely have forgotten what it means too.

So let's do a before and after comparison showing how the DB comment can help. So again, we see there's no context here. But after using this self-documenting style of model with the DB comment, we actually get the comment in pgAdmin.

If we look at the HasBled score, well now we can see that it is also a range from zero to nine where greater than three indicates high bleeding risk based on FDA guidance from 2019. So the solution now presents itself because there's context being put into the database for the ETL developers for doing dimension creation and for report developers that need to report on that. And after self-documenting inside of PGAdmin we can see the comment there again.

One of my favorite examples though is more complex. JSON fields that can change wildly over time with different keys. And in this particular case, the DB comment added was giving you what the keys are, warfarin allergy, bleeding disorder, pregnancy status, and that they're only in there as Boolean values. So now data analysts know the JSON structure without having to dig through the Django code to determine what's actually going to be in here.

This is great because we now have better documentation, actual documentation inside of the database for what our fields mean. And this can allow the ETL developer to potentially say, great. Well, let me take the keys that are inside of that JSON field and split them out into specific flags on a dimension to make it easier for a data analyst or report developer to report on them.

Now we can talk about these two features working together. You don't have to use one and not the other, and in fact, I would say you should probably use both. Here we can see the help text and the db comment, both providing context on what the range is, but one of them is geared, the help text, towards the actual data entry by the user. Whereas the DB comment is again to help the person or the developer that's going to be using the data later on after it's been entered into the database.

The help text lets the user know what the range of value should be, but we still want to have validation there on our forms, right? We can see that we should use both because they serve different audiences.

Now, another feature for self-documenting databases, also introduced in Django 4.2, is the dbtable comment. Again introduced in Django 4.2, it allows you to add a comment to the table, or the model. Per the release notes, it says, "The comment on the database table to use for this model. It is useful for documenting database tables for individuals with direct database access who may have not been looking at your Django code."

Now we can have complete context at our table level documentation. We have information about what the table is. It's a cardiovascular risk table, calculations per the Joint Commission, and the owner is the cardio team. But even better than that, we know who to contact. There's an email address there. So we have a what and a who for this table.

Again, because pictures are awesome, we can see how this looks inside of PGAdmin, where you can see the actual details about the information on the table.

So we have full documentation for everyone. Our end users get the help text, which is helpful for them. Our developers, our web developers, get help text and DB comments, which is helpful for them. But for our database administrators, our auditors, our data analysts, our ETL developers, our report developers, our data scientists, giving them access to the DB comment allows them to more fully appreciate what these fields mean.

So hopefully I've convinced you that this is the way. How can you get started? You can start today by doing an audit. Identify your top 10 confusing fields. Look for fields with cryptic names or complex business logic and start with your top 10 most confusing fields. You could also look back at some of the retrospectives you've had over the last three or six months and discussions that you've had internally about why was it so hard to support this particular implementation? And if it was driven by a misunderstanding or lack of understanding about specific fields added, those are good candidates.

Then start your documentation. You're only going to have to do this once, so do it the best that you can. Find out everything you can about the specific confusing fields and put it into a distilled DB comment, which allows the users of the database to appreciate what that field is. Provide business context. Provide compliance notes if necessary.

And finally, standardize. Once you've gotten through your first 10, you'll have a good sense of what that workflow should look like, and you can start to incorporate it into your code reviews, into any checklists that you might have. You may even start finding yourself wanting to write tests that check for this missing DB comment and having them fail if it's missing. When you do this, you really start to make documentation a habit and not an afterthought.

The documentation in particular we're talking about is for the database. But you should also do this for DB table comments, right? Because you have a similar thing here to the DB comment where audit your top 10 confusing table names or models. Maybe they were created so long ago that no one really knows why it is they decided to call it I_7542, but it made sense then. No one understands why now. Identify who the owners of those tables are as well.

Second, add the DB table comments to these models. Include business context and table owner details if you have them. Like we saw in the example, the cardio team.

And finally, standardization. Make this a part of your process. Update your code review checklists. Potentially look at adding tests that will fail if the DB table comment is missing.

Hopefully I've been able to convince you of the power and usefulness of the DB comment. And that you can make documentation a habit and not just an afterthought.

Thank you so much for your attention. I hope this simple yet powerful feature can help reduce some of the database confusion in your teams. Remember, documentation isn't just about helping others. It's about helping your future self six months from now when you're trying to remember what that field or that model was supposed to do.

Enjoy the rest of DjangoCon. You can find me at various places on the internet. I'll leave this up here for a couple of seconds for you all, and then if you have any questions, I'd love to take them. Thank you so much.
