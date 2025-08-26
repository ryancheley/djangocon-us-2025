All right, thank you. Good afternoon, everyone. Thank you for coming to my talk: "Django as Database Documentation Tool: The Hidden Power of Model Comments."

I am Ryan Cheley. I am a member of the Django Commons admin team with Daniel, Lacey, Storm, and Tim. Some of them are out in the audience. Hi, everyone. I've also been a navigator on Django Not Space. Session 5 is coming up, so if you have an opportunity and want to learn more about that, come see me or any one of the Django Not Space people. I'm more than happy to talk to you about that. I'm also one of the maintainers of Django Packages with Jeff and Maksudel. Hey, Jeff. I've been working with Django for seven years, Python for eight years, and I've been working in healthcare for 17 years. These are mind-blowing numbers for me, so just something to keep in mind.

Why am I going to give this talk? Well, I believe in the importance of documentation and the great benefit that it can have for intra-team, but also inter-team communication. I'm going to go through an actual real-world scenario that I've seen play out more than once.

So, a typical Slack conversation where the web developer posts into a channel: "Just pushed up new fields, CHADS score to the patient risk model." Now this seems pretty innocuous, right? Seems pretty innocent. But then we start to get some cross-team confusion.

The ETL developer who's responsible for getting that data out of your production database into a data warehouse asks the question: "Hey, I need to add this to a risk dimension, but I also need to document what it's used for." And then a report developer says: "Hey, yeah, and someone was asking me about this, and I can't add it to the dashboard until the ETL developer can add it to the data warehouse."

And so this is where the pain starts. There are teams that need to know about what this field is and they need clarification about what that field is. And they've asked the question and maybe three days later, maybe three minutes later, but some period of time later, we might actually get an answer from our original web developer.

Now it could be that the web developer had to go consult their notes, find the business analysts that they worked with, find the subject matter expert that they worked with. So the amount of time it took to get that answer is reasonable, but there's still a delay in getting that answer. And they finally respond back with this very opaque message: "It's the CHA2DS2-VASc Stroke Risk Score."

Now, we had to wait a while, three days, three hours, three minutes, whatever, to get that answer. But I don't know that we're any closer to really understanding what that field is for. At least, not really. Not in any sort of real sense.

And so there's a real cost here, right? There are delays in the construction and implementation of ETL pipelines. There are report development getting blocked because of ETL pipeline delays. And the web developer, the one that initially put out that message had to go find a subject matter expert, find a business analyst, find their notes to be able to get that answer and put it into the Slack channel.

So let me be clear, this is a real business impact, right? This isn't just a minor inconvenience. These delays to dashboard creation can actually have impacts on real decisions that are going to be made clinically for healthcare or from a business perspective if that's what this had been about. So productivity suffers across all teams, right? Not just the people who had posted the question, the new field, and not the people asking the questions afterwards to get clarification.

And so let's take an example of what a current state model might look like. And if we looked at it inside of Postgres with a create table statement, we can see that we have a very clean, very functional create table statement here, but it's also completely opaque. Yes, there is a field called HAS-BLED score. What does that mean? There is our QRISK3 value. I don't know what that means either. And this new field that we added, CHADS score. Again, we don't really know what these fields mean. We might be able to guess it, but we can't know for sure.

And so as a database administrator, when you might be looking at this, you have no idea what this field is, why it's important, what it might calculate. So what do these cryptic fields actually mean? And this is the root of our actual problem. The database itself contains no context around the business need or the clinical need, and that's the problem we want to try to solve here.

So quick show of hands, how many people knew about the comments that are available on fields in PG Admin? Quick show of hands. All right, great. So at least one of you. So how many of you have ever seen that field filled in with any meaningful or helpful information? Oh, good. There's one of you out there. Great.

So, but not all of you knew about it. And those of you that did know about it, not all of you have seen it filled in. And so this identifies a real gap in documentation.

And we should acknowledge at this point that our code comments are not database documentation. We should also acknowledge that despite our best efforts, any documentation pages we have on a wiki or in Confluence or whatever can get stale. A code change gets pushed up, you forget to update the documentation.

And also, undocumented expertise does not scale. On a small team of three or four people, it might be okay, well probably not, it might be okay that when someone asks a question, "Hey, what does this field mean?" Oh, go ask Sarah. She knows. But what happens when you have 8 people, or 16 people, or 32 people? What happens when you have more than one person named Sarah? What happens when no one actually knows who Sarah is because Sarah doesn't work in the IT area or the development area anymore. She works in an entirely different organization now and no one knows how to get a hold of her.

And in healthcare where I work, there is an actual need from a regulatory perspective to have these comments on the fields to show to auditors what it is that we're collecting about our patients and to be able to show them that we know what these fields are and what they contain.

And I can hear some of you out there saying, "But hey, Ryan, there's that help text. Why can't we just use that?" But there is a limitation that I think we should all acknowledge here, which is that the help text doesn't solve this problem because it's designed for guidance for end users. Those are the people that are entering the data into our system. These are not the people that are going to be trying to figure out what the underlying business context of it is. And not everyone has access to the front end of an application or even to the Django admin to be able to appreciate the help text. And so it's a good tool, but for the wrong audience.

And it's at this point, we can see an example of what that help text might look like. And we can see that okay, yeah, it's the CHADS-VASc score for stroke risk assessment, 0 to 9, and a higher score means a higher stroke risk. Again, that helps the user entering the data, but it doesn't help anyone who might need the backend context behind that.

So it's at this point we should acknowledge that we have different audiences with different needs, different stakeholders, if you will. We have end users who need guidance on data entry in the form. And so the help text is a great thing for them. Any sort of comments related to the database, well, not so much.

The web developers, well, they're going to need to know about the field's purpose. And so help text is maybe it's helpful for them. Maybe it's not. But any sort of comments around the database itself would be super helpful.

DBAs are database administrators. They want to know about the schema. The help text is going to be completely unhelpful for them because the chance of them actually having access to the front end is probably lower or non-existent. But comments in the database are helpful.

And auditors, as I mentioned before, from a compliance perspective they need to have that information. The help text, it might be helpful for them, but what's most helpful is going to be database context.

And data analysts are going to need to know the context around the database itself. Help text is not useful, database comments would be.

And so where the help text falls short is that a data team that is using SSRS or Power BI or Tableau or insert your visualization or reporting tool here, they can't see the help text. Regulatory auditors, they routinely examine the database directly and they're not going to have access to Django admin or the front end. ETL developers building data pipelines without field context, again, they're not going to know or be able to access the help text.

But in Django 4.2, we introduced db_comment, which was, as I said, came out with Django 4.2 in April of 2023. And so a quick show of hands, how many of y'all have used this feature before? Oh my goodness, you've been doing everything. This is amazing. If there are any questions I don't know the answers to, I might come to you later. Okay.

And so this is an example of what that db_comment might look like on our CHADS score field. It has a very robust description here giving a range value. Some of the same information that we got from the web developer initially, but also adds a little more context. Here it does range from zero to nine, but a value greater than two indicates anticoagulation considerations and is based off of the ESC guidelines from 2010. Lots of context information here.

And just notice how clean this is, right? We just add this db_comment with a description of what the field contains, and we know so much more about this field. And it's available to the developer who was developing the web developer who was making the page. But as we'll see later, this is also then put into the database for those that have direct database access.

And the magic happens when Django generates the migration, because it puts this comment directly into the database where anyone with database access can see it. Which means that the database documentation lives in the database itself. Let me say that differently: The documentation lives in the database itself, so people can appreciate what these fields mean.

And just a quick review of what this might generate. It would have our create table here, but then it also adds this comment on column, which takes the exact same content that we put into the db_comment attribute on our patient risk model. And it's going to add this comment directly into pgAdmin, which again means that anyone who can query the database can now see this documentation.

And this is what it would look like inside of pgAdmin. We have that comment that not everyone in the room knew about it. We have that comment filled in, which not everyone had seen. And so before we had these mystery fields where ETL and report developers might not have any idea what the fields represent. And let's be honest, the original developer who made all of this in three weeks, three months, in a year, they're probably not really going to remember what it is either.

So let's do a before and after comparison showing how the db_comment can help. So we've got our basic logic here. It defines what each of the field types are. We've got some integers. We've got a JSON field. We've got decimals. And it's clean and functional, but it doesn't tell us anything about the business logic, about the business context. And again, any ETL developer looking at this, they're not really going to know: What does CHADS score represent? Is it a count? Is it a percentage? Is it a risk level? Is it unbounded? Can it be negative? None of that is here. This also means the report developer can't build meaningful dashboards because they don't really know anything about this information.

So let's start adding some db_comments. Take our CHADS score and we put in our comment here that it's the CHADS-VASc score risk from 0 to 9. Greater than 2 indicates anticoagulation considerations based off of the 2010 ESC guidelines. Again, this gets put directly into pgAdmin.

But what about the HAS-BLED score? Again, we didn't know what that was before, but now we can see that it's a bleeding risk that goes from 0 to 9, similar to the CHADS score, where greater than 3 indicates a high bleeding risk based off of FDA guidelines from 2019. And so now, again, full context for ETL dimension creation and report development. And this is what it will look like in pgAdmin.

I think one of the most interesting examples, though, is when we look at a JSON field. Because here we can see, based on this documentation on the db_comment, what the keys are in that specific JSON field. Which means that we don't have to go digging around for it. One of them is pregnancy_status. Well, now we know that it's pregnancy_status and not something like is_pregnant, pregnancy_YN, pregnancy_01. Any one of those things that it might be based on the fact that it's a Boolean value. But we also know that each one of these keys is only going to contain Boolean values. So now we don't even have to try to check those things. We know that from the documentation.

And so this matters because the ETL developer knows without having to dig through all the code what this JSON field contains and what it represents. And then knowing that, they can start to extract that into actual attributes on a field or on a table that can then be used in report development later on. So then the report developers don't have to go digging through and extract out all the keys from the JSON field. And this is again what it looks like inside of pgAdmin.

So we now have this concept of the db_comment. We also have talked about help text. And you might ask, well, should I do one and not the other? I'd say do both. Both fields working together help to provide full context. Remember, the help text is to provide user form guidance on data entry. The db_comment is for database users. And so from a best practice perspective, I would argue that you should use both of them because again, they serve two different audiences.

Okay, this is great, Ryan. We can do this on our fields, but what about tables? Because sometimes the tables are super confusing too. And yes, you're right. And fortunately, in Django 4.2, we also saw the introduction of db_table_comment, which allows us to add table comments. And so we can now get complete context at the table level from a documentation perspective.

We can add a meta class to our model class with a comment about what the table is. And you'll find out what works best for you. But what I have found is that you provide something like this: This is a cardiovascular risk calculation per the Joint Commission's PC-03. And the owner is CardioTeam at Example.com.

And so again, we have table level documentation, and in this particular case, we have a what and a who for this table. We know what this table is about. It's about cardiovascular risk, and we know who owns it. The cardio team owns it, and we know how to contact them if we have any specific questions about this table. And looking inside of pgAdmin, we can see this comment added at the table level in the comments. And so again, we have full documentation for everybody when we start using both help text and db_comment and db_table_comment.

Okay, maybe I've convinced you that this is the way. Maybe you want to get started, maybe even today. How do you get started? Three steps:

Audit your existing models. Look for fields with cryptic names or complex logic. And start with your top 10 most confusing fields.

Then you want to document it. If you do this really well and write, you only have to do it once. Get as much information as you can about the comments and about the tables, and then distill this into a short sentence or sentences you can put into the comments.

And then standardize. Make this a part of your standard practice. When new columns get added, make sure they have db_comment. Maybe even add a couple of tests that check for these db_comment missing and they fail when they are missing.

Similar to db_comment, you can do the same thing with db_table_comment. Identify your top 10 most confusing tables. This can come out of retrospectives where maybe an implementation didn't go so well and there was lots of confusion about it and no one really knew who to talk to about it. Start there. Again, do as much research as you can to get the best context, distill that into some short sentences or sentence, add to the db_table_comment, and then make it a part of your standard code review process, make it a part of your process in general.

I hope I've been able to convince you of the power and usefulness of db_comment and db_table_comment, and that you can make documentation a habit and not just an afterthought. Thank you very much. I hope that this simple Django feature can help reduce some of the database confusion in your teams. And remember, documentation isn't just about helping others. Sometimes it's about helping yourself three months from now, six months from now.

You can find me online at these various places, and I'll take questions now. Thank you so much.
