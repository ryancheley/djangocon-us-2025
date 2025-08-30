All right, well good afternoon and welcome to DjangoDB Comment: Self-Documenting Databases. I really am excited to be here at DjangoCon US 2025 and talk about a simple but powerful Django feature that came in version 4.2. There'll be time at the end for questions and I look forward to hearing those.

Who am I? I'm Ryan Cheely. I am the associate vice president, yada, yada, yada. I've got 17 years of experience in healthcare with eight years of experience with Python and seven years in Django.

So why this talk and why now? Well, I believe in the importance of documentation and the great benefit it can have on intra-team communication. So let's look at a specific example that you may have seen at work. I know I've seen it where I work.

A web developer posts in a Slack channel or Discord or wherever just pushed new field Chad's score to patient risk model. And this looks innocent enough, right? Like, okay, great. We have a new field called Chad's score in the patient risk model. All right, fantastic.

But then the ETL developer on the team says, all right, cool, I need to add this to the risk dimension. But what does it calculate? The report developer says, yeah, I'm going to need this for a dashboard I'm working on. Do we know anything more about this?

So this is where the pain starts. Multiple teams, the ETL development team, the report development team, are now blocked and waiting for clarification. And for those of you that know about SpongeBob SquarePants, this may look familiar. Because at some point, maybe 30 minutes, maybe three days later, the web developer comes back and says, Oh, well, it's the CHA2DS2-VASC Stroke Risk Score. So we had to wait a while to get that answer. And we still have no idea what this field is for.

And there are some real costs associated with this delay while we're waiting for information on this specific field. The ETL pipeline is delayed, right? The report development is getting blocked on dimension requirements. We are losing developer productivity across all teams. So this isn't just a minor inconvenience, right? This is an actual thing. The other issue here is that you can have regulatory compliance challenges, which is a real issue in healthcare where I work. Auditors need to understand what data we're storing and how we're using it.

So let's take a look at an example of what this patient risk assessment model table might look like. Seems simple enough. We've got an ID, we have this CHADS score that we were just talking about, but there may have been some other fields before there too. This Has Bled score, a QRISC-3 value, a contraindication flag, a last calculation date. So it tells us what fields are there, but it's kind of opaque, right? If a DBA were to look at this table, they would not really have any idea what these fields mean or why they matter.

So the root problem here is that the database itself contains no business context. What do these fields actually mean for the business? And so we've identified a documentation gap. And I'm sure we've all known this, but to actually see it is palpable, right? Code comments are not database documentation. Try as you might to keep your knowledge management system, wiki pages, whatever, up to date. They're going to get stale over time. Also, this undocumented expertise, maybe there is someone on the team that knows what the CHAD score is. But this undocumented expertise doesn't scale well.

When you've got three people, yeah, not writing it down is probably not that big a deal. You get up to six people and like, well, maybe it's not such a big deal, but it might be getting there. You get to 12, 24, 48, and suddenly no one really knows, nor can they ever really know what that field is about. And again, in healthcare, we have this regulatory need for field level documentation.

Now, I can hear some of you out there maybe ask quite rightly, well, but what about the help text, right? Like it's there, it's been there for a long time. Why can't we just use that? And we can see an example of what that might look like inside of our patient risk model here if we were to add it to our CHAD score and we can see a help text here that says enter the patient's CHA2DS2-VASC score.

Now even if that was helpful to you it's only visible in the Django admin forms on the help section or in the data entry forms on the front end of the application. Report developers, ETL developers DBAs may not have access to these front-end applications and so this help text isn't really going to get them what they need. So it's the right tool but for the wrong audience and this is where we acknowledge that we have different audiences that have different needs different stakeholders if you will.

Our end users need form guidance and the help text is well helpful. A DB comment they're never going to see it. They're not going to care about it. Now our developers, our web developers, will need to know field purpose and so the help text might have a little bit of context and helpfulness to it but really the DB comment is going to be more helpful for them in the end.

DBAs, similarly they need to understand the schema. The help text is unavailable to them but DB comments are like gold. Auditors need to look at compliance documentation. They may be able to access the front end, but chances are they're not going to. And so again, the DB comments are going to be the most helpful thing for them.

And finally, data analysts, data scientists, report developers, anyone that is consuming this data to be able to then do something else with it afterwards. Well, they're going to need direct database context, and the help text, again, is not going to be there for them. And so we're going to want to rely on these DB comments.

So we're kind of seeing where help text falls short. Our data team who might be using SSRS, Power BI, or Tableau, they can't see the help text. On database migrations, there's no context for the schema changes. Legacy system integrations, their external tools are going to need field documentation. Again, coming back to regulatory audits, the auditors are going to need to examine the database directly. They're not going to be looking in the Django admin. And kind of going back to what started it all, cross-team collaboration, the ETL developers building our dimensions are going to do this without field context. And so it's just really hard to use and rely just on the help text.

Enter "db comment introduced in Django 4.2". We can see here, very similar to what we saw before, but instead of having the help text, we have "db_comment". And we can see here that this comment "chad_vasc_risk_score_calculation". Now the magic is going to happen once the migration occurs that puts this comment directly into the database itself.

And we can see here now that the documentation is going to live inside of the database itself using this db comment. And what this generates is this particular PostgreSQL where we have a comment on the column which matches the DB comment. And now the results are that anyone querying the database can see the documentation.

Before as we saw we had these mystery fields. We knew what types they were. CHADS was an integer. Hasblood was an integer. Contraindications was a JSON field, QRISC3 was a decimal. But there's no context, no idea for what these fields represent. And honestly, even the web developer doing the development is probably going to forget what these things mean in a week, in a month, in a year.

Now, afterwards, once we start adding the DB comments and start putting in a little more context for this CHAD score, we can see that it's a stroke risk that goes from 0 to 9. A greater than 2 indicates anticoagulation considerations per the 2010 ESC guidelines. And the HasBled Index, well, it's also a scale from 0 to 9 that talks about bleeding risk, where greater than 3 indicates a high bleeding risk based on FDA guidelines from 2019.

So now the result of this is that the context for ETL dimension creation and report development is where it's going to end up needing to be, which is in the database itself.

Now consider a more complex example, a JSON field. Here we can see that by adding a DB comment that indicates what the keys are going to be, in this case a warfarin allergy, a bleeding disorder, or pregnancy status, and that they're all Boolean values. So now as the ETL developer or as the report developer or data scientist or data analyst or whatever, you have a lot more information about what that field is going to have. And perhaps as the ETL developer you can actually take out those keys and put them into their own columns to make it easier for the report people, the data people to do what they need to do to analyze the data.

So this matters because now data analysts, whoever's using the data can know the structure of the JSON without having to dig around through the Python code, the Django code that generated the form where the data entry occurred.

So in addition to the DB comment, there was another attribute added called DB underscore table underscore comment, where you can add comments to the tables themselves. And the power here is that you can document what the purpose of the table, the model, that turns into a table really is, you can document what kinds of jobs run, the frequency with which they run, and almost probably the most important thing, who owns the data that's in it.

Here we can see that this particular patient risk model, it's a cardiovascular risk calculations for the Joint Commission, which is updated nightly via the clinical calc job, and the owner is the cardio team. So if I have questions now, I can go to the cardio team.

Now, if we wanted to look at what the migration for this would look like, we can see here that the DB comment is just included as part of the migrations, but this isn't super interesting necessarily. But these are just comments. So there's no, they're just metadata. There is no data loss.

Now, we can start talking about the power of the help text with the DB comment. Here we can see the CHADS score has a help text, which says to enter a score from 0 to 9 based on patient risk factors. And the DB comment itself says that it's the CHADS-VASC risk score, which goes from 0 to 9, with a greater than 2 indicating an anticoagulation risk, and it's based off of CMS 134-V8. So, from a best practice perspective, I would say use them both because they serve different purposes, different stakeholders, as we saw on that table earlier.

And now you might be wondering, well, this is all great, Ryan, but what does it look like inside of the database itself? So if we were using pgadmin, we might see this as a database administrator or someone with direct access to the tables before the introduction of db comment, where I have a name for my field, but not much else. And then afterward, with that full comment that was entered into the model by the web developer. And again, for the HasBled score, we have comments. The QRISC3 value, the comments come through again. And finally, for the contraindication flags, all of the data surrounding that flag, the keys that exist inside of that JSON field.

And so I would encourage you to start today. But where do you start? Well, identify your top 10 confusing fields. Go through an audit. Maybe it's your last couple of retrospectives. There's a set of data that keeps coming up as being super confusing, not only to you as the web development team, but the ETL developers on the data pipeline team or your data analysts. Someone is confused about a field somewhere. And so find those, document those, and then start adding the DB comment to them with business context and compliance notes to make them more meaningful to the people who only have access to this data through a database.

And then standardize. As you start seeing how powerful and useful these are, make sure to put it into your code reviews. Make sure that it's part of that code review that happens. You could even potentially start adding tests that fail if the DB comment is missing, or if it's there but it doesn't have a specific length because maybe you think that the length is important.

And so now we just have a couple of code examples. You can download all this code with this QR code, and you can find me online at these various spots. I'd love to hear about your database documentation challenges and successes.

Any questions?
