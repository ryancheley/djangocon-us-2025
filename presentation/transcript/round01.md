Speaker 1
Good afternoon everyone. I would like to welcome you to my talk, Django DB Comment: Self-Documenting Our Databases. This was a feature that was introduced in Django 4.2, and I'm going to talk a little bit more about ways that I think it can be super helpful and useful to those of you that have report developers, data scientists, data analysts, or ETL developers on your teams and you want to effectively communicate what some of the fields in your tables or models are actually supposed to be for.

I'm Ryan Cheely, I am the Associate Vice President of Business Informatics and NextGen Support Services at my day job. I've been in healthcare for a little more than 17 years. I've been using Python and Django for eight and seven years respectively. Different places you can find me on the internet. I'm most active on Mastodon, but I do blog every once in a while at RyanCheley.com.

So why this talk? Why now? Well, I believe in the importance of documentation and the great benefit it can have on intra-team communication. I think also in inter-team communication, it can be very, very helpful as well.

So let's go through an example of some potential cross-team confusion. Web developer posts to Slack, "Just push new field CHAD score to patient risk model." The ETL developer asks, "I need to add this to the new risk dimension. What does it actually calculate. Like, what is it for? What does it tell me?" The report developer says, "I also need this for a dashboard, but I need the specs on this before I can fully integrate it into that dashboard." And the original web developer, maybe 30 minutes later, maybe a day later, comes back and says, "Oh, it's the CHA2DS2-VASC stroke risk score." Still doesn't tell me what it is though. No links, nothing. Just a little more of a definition there.

So some cross-team confusion here between, in my case, the data ops team, that's where the ETL developer lives, the report development team, that's where the report developer lives, and the web development team, that's where the developer lives. So we have this CHAD score, but we don't actually know anything about it for this new dimension.

So the real cost here is delays in ETL pipelines while the developer is waiting for field clarification. Delays in report development for dashboard creation. Again, waiting on a definition of what this field actually means. There are developer productivity losses across the team. The original web developer has to stop, go back through their notes, write something up. Let the ETL developer and report developer know in Slack, well, this is what I think it is based off of the conversation that the business analyst had with the subject matter expert over in the clinical areas. All wasted time.

There could also be some regulatory and compliance challenges based on the particular environment you're in, the particular sector you're in. As I said, I'm in healthcare, regulatory compliance stuff is super important, and being able to tell an auditor what a field means has a lot of value. So as we can see, hopefully, this cross-team dependency is creating bottlenecks in the workflows.

So I'm gonna show you the current state of this patient risk model that we had seen before. And it looks like this. If we were looking at it today, inside of the raw SQL, on this table patient_risk_patient_risk_assessment. It's got an ID that's the primary key, a CHADS score, a HAS-BLED score, a QRISK3 value, and then the last calculated date.

So I can see that there are fields here related to patient risk assessment, but as a non-subject matter expert, I may have literally no idea what any of those values mean. Right? What do any of those mean? Even with the description that we got before from the web developer.

So there's a documentation gap. We all know that codes in our code comments are not the same as database documentation, right? Anything you put in your code does not necessarily make its way over into the database that we're using. We also know that despite our best efforts and potential workflows, there is the potential for wiki style pages of documentation to become stale.

Another thing is that when you are a small group, that sense of common knowledge about what everyone knows could be fine. Three people, four people, maybe five people, you're going to be okay, mostly. Get up to 10 people, 20 people, 50 people. That common knowledge doesn't scale. Making sure that everyone knows what those things mean is super hard, unless you write it down somewhere.

And again, coming back to, in my particular case with healthcare, the need for field level documentation for a regulatory audit. So as we can see, there is this gap. We have documentation that might live inside of the code that we've written, but it mostly, almost never, lives in the database where people who only have database access would be able to actually use it.

But what about the help text, Ryan? I hear you all asking why can't we just use that? Well there are some limitations right? We could add to the CHADS score a help text which says in this case "Enter the patient's CHA2DS2-VASC score." This is great but this is only visible in the Django admin or on a front-end user form provided you've actually made that accessible. To let people who are doing data entry into the database know what that field is for. It doesn't help the people who are going to consume that data later on.

So we have different audiences here and they all have different needs. Our end users are one stakeholder who have needs of knowing what data needs to be entered in and any potential ranges those values might need. The help text is super helpful for them here right, because that's what's going to be displayed on the form. DB comment, that's not going to be displayed anywhere so they don't need it.

Developers, the web developers we started off with, well they need to know what the purpose of the field is and that help text could be a limited bit of help to them but it doesn't provide full context really. That's what the db_comment is going to be.

And again, DBAs, they need to know about schema docs. They want to be able to make sure that they know what these schema mean. And so the help text, again, it's going to be embedded in the model. It's not going to be in the database. You're going to want the database comment.

Report developers, field definitions, very similar to the developers at the top. The help text is not going to be helpful to them. The DB comment will. And the data analysts or data scientists who want to know more context around the fields that are existing in the tables in your database. Help text, not so much. DB comments, yes.

So hopefully you can see here the help text is helpful but only for people who are entering data into the database, into the system. For those of us that are trying to actually consume data for other reasons outside of the specific application, the DB comment is what's going to be most helpful for us.

So as we can see where the help text falls short, the report development team using SSRS or Tableau, they can't see the help text. They're not going to the front-end application. For database migrations, there's no context for schema changes. And cross-team collaboration, well the ETL developer building the dimension is going to do it without full context because again the help text is something you would see on the front end of the application not something you would see in the database.

And you might ask well won't everyone have access to the source code? Maybe, but you cannot rely on data scientists, data analysts, ETL developers, report developers, non-web developers to go spelunking through your web code just to find a definition of what that specific field means.

So introducing Django's db_comment released in Django 4.2. And what it does is it adds a new attribute here called db_comment where you can put in specific information about that specific field. Now this looks very much like the help text but it doesn't just live here, it also makes its way into a database if that database is supported.

So now finally, the documentation about the field lives in the database itself because we put it into this db_comment here. So it's also living in our web code. And that particular model there will generate this SQL statement if we were to use Postgres. It would create the table, give us a CHADS score, and then it would create a comment on column and it would give it that comment that we had added.

Now I had said this works on databases that are supported. Postgres is supported as we can see from this example, Oracle is supported, SQLite is not. So now anyone that can query the database can see the documentation.

So when we look at the before state when we had those mystery fields, CHADS score, HAS-BLED score, QRISK3 value, contraindication flags, we don't really know what any of those mean, why any of those are important. Which means the ETL developer has no idea what these fields represent. The report developers, the data scientists, data analysts, they don't necessarily have any ideas either. Or worse, they all have a different idea on what each field means.

So after we introduce the db_comment and have self-documenting models, we can see this. Well, the CHADS score is a stroke risk that goes from 0 to 9 with greater than 2 indicating anticoagulation consideration per the 2010 ESC guidelines. We have so much more information about this field now. So much more context.

The HAS-BLED bleeding risk. Well, HAS-BLED is a bleeding risk which goes from zero to nine. A greater than three indicates a high bleeding risk per FDA guidance from 2019. Again, so much more context. The report developers will understand this is a bleeding risk index and what the thresholds are. They can probably then incorporate that into their dashboards to make them more visually appealing.

The QRISK3 cardiovascular risk. Wow, so that QRISK3 was a cardiovascular risk score. I didn't know that. But now we can see that it's a 10-year CVD risk percentage from 0 to 100. Used for statin therapy decisions based off of some NICE guidelines. So now we have a complete picture about those fields. Different teams and every different member of those different teams can look when these comments go into the database and know what these fields are about.

Now there was one field that we didn't really talk about too much. It was a JSON example. But again, we can put more descriptive data in the db_comment to let people know, well, yeah, this is a JSON field. And if you don't know what keys are going to be in there, like, you know, good luck trying to figure it out.

But this tells us that that contraindication flags as a clinical contraindications per CMS 134v8. Its keys are warfarin allergy, bleeding disorder, and pregnancy status, and they're only Boolean values. So now when we look at the data, if we need to extract out, say, pregnancy status as a true-false, it's much easier to do because we know that that's a potential key in there versus having to guess, well, is it pregnancy? Is it pregnant? Is it pregnancy_YN? Is it pregnancy_? No, it's pregnancy status. It's going to be a Boolean value. So now, as I said, everyone knows what the structure is supposed to be.

So now if we look at the complete context of table-level documentation, in addition to having db_comment, we can also add db_table_comment, which then describes what the patient risk assessment table is doing, or model, is doing. So in this case, it's a cardiovascular risk calculation per the Joint Commission. It's updated nightly via clinical_calc_job, and it's owned by the cardio team.

I now know everything I need to about this table. I know everything I need to about the fields in this table. I have full descriptions that are going to be in the database. I know who the owner is, so I can contact them if I have a question or something just doesn't look right to me.

And this is what a migration would look like if you ever wanted to dive into it. You would see some very familiar things if you've ever dug into those migration files before, but now in addition to what you have seen before, you would also see this db_comment with the description there. And this is all just metadata, so there's no data loss.

But now when you combine the two of them, they work together really, really well. You can have a help text, which tells the user what should be entered into the field and some descriptors about it. You can also have validation that prevents someone from entering a score below zero or above nine, which you should totally do. We've also got the db_comment here, which is telling us, as database users, what this field is actually for. So use both of them when you have the opportunity, because they serve, as you'll remember, two different sets of audiences, two different stakeholders.

And this is where I'll have an image showing what the comments inside of the database will look like. And we can see here this allows the DBA to understand the fields without calling the web developer, without calling a subject matter expert who may or may not be even knowing what they're asking about. I have this field, QRISK3_value. Do you know what that is? I have no idea what that is. Well, when it's in the table that you own, I have no idea what that means.

And it's easy. You can start today with three simple steps. Step one, identify your top 10 confusing fields. Now, this may or may not be super easy, but if you look back at your last retrospective or last meeting where there's a lot of confusion about a specific topic or item, look at all those fields. These would be good candidates to start adding these DB comments to.

Once you've identified them, start adding the db_comment with business context and compliance notes, right? This will be the last time you have to figure this out. So go all in. Figure it out as best you can. Figure out a specific structure that you and your team agree to in terms of how these DB comments should be constructed to make it as easy as possible for the end users of them, that is people with read-write access to a database, to be able to appreciate the information that is there.

Standardize. Update any code review templates or checklists or processes you have to include checking for a db_comment. You could also potentially add a test that fails if db_comment isn't on a field, which would then be enforced on everything, so you'd have to do it for everything all at once potentially, but, you know, those are some options.

And then some resources to help get you started. The example code that will be all in here. I'll have the documentation to Django, the documentation to the table comments, the original request, which was ticket 18468, and the release notes from Django 4.2.

Speaker 2
If you have any questions, I would love to hear them. Thank you so much.
