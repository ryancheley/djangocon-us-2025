Welcome everyone to DjangoCon US 2025. I am excited to talk with you about a simple but powerful Django feature that can transform how your team works with databases.

A quick intro about me: I'm Ryan Cheely. I have been in healthcare for 17 years, building systems that help clinicians make better decisions for patients. I've been working with Python for about eight years and using Django for about seven years.

So why this talk? I believe in the importance of documentation and the great benefits that it can have on intra-team communication as well as inter-team communication. I'm going to walk through a real scenario from my team.

So let's talk through what happens when a web developer might add a new field to a model. They might post in a Slack channel pushed up the new field CHAD score to patient risk model. But then the ETL developer sees this new field and needs to add it to a data warehouse but they have no idea what it actually is. So they ask, "Hey I need to add this to the risk dimension table, but what does it calculate? What is it?"

A report developer might chime in and say, "Hey yeah they were asking to have this added to a dashboard as well but I can't really move forward until the specs for the dimension get resolved."

So this is where the pain starts because as some of you may have experienced you might post a question in a slack channel and then some period of time later an answer comes back and the web developer was taking their time maybe looking at their notes maybe following up with the business analyst who wrote up the use case, maybe going directly to the subject matter expert, and comes back with a very opaque answer. Well, it's the CHA2DS2-VASc stroke risk score.

So we had to wait for a while to get an answer, but I don't know that we're any closer to knowing what this CHADS score actually is or what it might be for. Stroke risk, okay, but what else is there?

So there's some real cost here, right? There are ETL pipeline delays waiting for field clarification. Report development is blocked, waiting for additional information to be able to use anything that's added to the dimension. The original developer, the web developer, has lost time going through their notes, reaching out to a business analyst, reaching out to a subject matter expert, trying to find out more information for the ETL developer and the report developer. So productivity suffers across all of the team, not just the original developer.

So let's take a look at a current state of what our database scheme looks like today. This is clean and functional, but it's also completely opaque. I mean, just look at these field names: HasBledScore, QRISK3Value, CHADSScore, Contraindication flags. If you don't know anything about cardiology or stroke risks, it might not mean anything to you.

Now imagine a DBA looking at this, a database administrator looking at this, and trying to figure out what this table might even mean. Right? So we have these mystery fields. We can see what the field names are, but we don't really know what they mean. And this is the root of our problem. The database itself contains no business context.

And when we look at the field inside of, say, pgadmin, we might see something like this. How many people have even seen a comment filled in in a database before? Yeah, okay. So, there's this documentation gap.

Why don't traditional approaches to documentation work here? Well, as we all know, or maybe we'll know now, code comments are not the same thing as database documentation. Code comments are great for developers when they're reading code, but they don't help DBAs or data analysts who are working directly in the database. Wiki pages, confluence pages, whatever, can get stale quickly. Someone updates code, but forgets to update the documentation.

Undocumented expertise doesn't scale well. The statement "we'll just ask Sarah, she knows" might work in a small team of a couple of people, but as that team gets larger and larger, you have a single point of failure. And all of a sudden, maybe no one even knows who Sarah is to figure out how to reach out to her because there are multiple Sarahs. Pause for laughter.

And in healthcare where I work, we have regulatory requirements. Auditors ask questions about field level documentation to understand what data we're storing about patients.

But you might ask, I can hear you all out there, what about the help text, Ryan? That seems like it could solve this particular problem. But it doesn't. Help text is designed for end users that are filling in forms. It's UI focused guidance.

The problem here is that it's only visible in forms, either in admin or on the front end. But if you're a DBA who's using PGAdmin, or a data analyst using Tableau, or an ETL developer building data pipelines, you'll likely never see the help text. It's the right tool for the wrong audience.

And here's an example of our form. We can see CHAD score, HasLED score, QRISC3 value, all with helpful help texts below them, but only the data entry folks are ever gonna see this.

And it's at this point we have to acknowledge that we have different users with different needs. Different stakeholders. We have our end users who need form guidance, and help text is exactly that. They will likely never need to look at the DB comments. Our developers, web developers, need to know field purpose, and so the help text might be helpful for them, but DB comments could be helpful for them as well.

Our DBAs need to know about the schema. So the help text is not available to them, probably wouldn't be helpful for them. DB comments would. And auditors are there to monitor compliance. They may never see the front end, so it's likely not going to be helpful. The help text is likely not going to be helpful, whereas DB comments will be.

And finally, data analysts who need to know the context around the database. The help text, probably not going to give it to them, but the DB comment will. Different audiences, different needs.

And so where the help text falls short is that our data team using SSRS, Power BI, Tableau, whatever, they can't see the help text. They're not going to the front end to read the help text. Legacy system integration, well our external tools need definitions and they're not going to see it from the help text. Again, regulatory audits. The auditors need to be able to examine the databases directly and not in either the Django admin or on the front end.

And cross-team collaboration suffers if we rely just on help text. As we saw earlier, the ETL developers building the dimensions without field context are just going to ask more questions so they can get clarification on what it is they actually need to do.

Here's the solution. In Django 4.2, we introduced the dbComment parameter. There's another parameter I'll come to later on, but I want to focus on dbComment first. This simple addition to the field definition puts documentation directly in the database scheme.

Notice how clean this is. It's just adding dbComment with a description of what the field contains. In this particular case, it says the CHA2DS2-VASC stroke score, which goes from 0 to 9, and a greater than 2 indicates coagulation consideration. This is based on the 2010 ESC guidelines.

The magic happens when Django generates the migration. It puts this comment directly into the database where anyone can see it. Our solution here is that the documentation lives in the database itself. Documentation that was put in there by the web developer. The documentation that was put there by the web developer and it was discovered by a business analyst or by working with the subject matter expert directly.

And what does this generate? Well, if you're using Postgres, it will look something like this. Some normal stuff that we've probably seen before, but the thing I want to call out here specifically is the comment on column. And this needs to be updated to match what was there before. But we can see the comments added here, the CH2DS2-VASC stroke risk score calculation.

The result here is that with this column, this comment added to this column, anyone querying the database sees the documentation. That comment is now filled in, and it looks like this.

Before, we had these mystery fields: Hasgled score, QRISC-3 value, contraindication flags, CHAD score. So this problem is that ETL and report developers, data analysts, DBAs have no idea what these fields represent. And further, I'd argue that in three months, six months, a year, the original web developer won't remember either.

So let's do a before and after comparison. Let's not. Oh yeah, let's do a before and after comparison. And now we can see with this afterwards when we've added DB comment, these comments are there for the web developer to see when they're looking in the code and we know that they go into the database afterward.

And here for the HasLED score. The result is that the context for ETL dimension creation and report development is available to those people that need it where they need it in the database.

And another example here is a more complex field, like a JSON field, that in this particular case has exactly three keys which are fully called out in the documentation that's going to be written to the database. Why this matters is that now a report developer, data analyst, and ETL developer knows everything they need to about the JSON structure without having to dig through the web development code.

And further, if you get really into it, the ETL developer can probably extract out of that JSON field three unique fields, flags, that can then be more easily used by data analysts or anyone who's actually looking at the data.

Now, I mentioned before another parameter that was introduced in Django 4.2 called a dbtable comment. And in this case, what it does is on the meta class for the model class, you can add a comment directly to the table itself. And in this case, we have comments that show what the table is for, who the table is owned by, and if we have questions about it, we know who to reach out to. It's the cardio team at example.com.

Now, both features, the help text and DB comments can work together, and they should. I think it's actually a best practice because here, the help text lets the user know what the range should be. Still want to have validation in there on the front end, right? But we've also got the database comments here, which tell us what we need to know if we're going to be looking only at the database itself.

I would say use both because they serve different audiences, going back to that different stakeholders slide from before.

So great, you've now found out about this fantastic new feature from Django 4.2 and might ask, well, how do I get going? You can start today with three easy steps.

First, audit your top 10 confusing fields. I'm sure this has come up at retrospectives or support tickets or whatever. However, find your top 10. Look for fields with cryptic names, complex business logic, whatever the case may be, and really find out what those fields are. Ask lots of probing questions, because you're only going to have to do this once per field, but it will pay dividends in the long run.

Once you have that, start adding DB comment with business context and your compliance notes. So you went through all the work to find out what these fields are, now start adding it to your db comments.

And finally, standardize the process for when adding new fields. Make it a requirement that every time a new field is added to an existing class, or any time a new model class is added, that this is just part of the workflow. Maybe you have tests that you introduce to check for the existence of db comment that fail if it's not there. So make documentation a habit, not just an afterthought.

I hope I've been able to convince you of the power and usefulness of DB Comment. And if I haven't, I look forward to talking to you afterwards. There are various places to find me on the internet. I'd love to continue this conversation after the talk. You can find me on these various platforms.

Thank you very much for your attention. I hope that this simple Django feature can help reduce some of the database confusion in your teams. Remember, documentation isn't just about helping others, it's about helping yourself, helping your future self, when you're trying to remember what a field is supposed to do.

Enjoy the rest of DjangoCon. I'm now looking for questions. Thanks so much.
